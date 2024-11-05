import asyncio
from fastapi import APIRouter, Body, status, HTTPException, Depends
import logging
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
import httpx
from app.schemas.passagem_schemas import PassagemSchema, PassagemSchemaList, DeletePassagemResponse, PassagemSchema2
from app.models.voo_model import VooModel
from app.utils.dependecies import DatabaseSession
from app.models.passagem_model import PassagemModel
from app.security.security import get_password_hash, verify_login_current, verify_password, create_acess_token
from uuid import UUID, uuid4

logger = logging.getLogger("uvicorn.error")
router = APIRouter()


@router.post(
    "/buy_ticket_no_login",
    response_model=PassagemSchema,
    summary="Buy ticket without login",
)
async def buy_ticket_no_login(user_id: str, db_session: DatabaseSession, passagem: PassagemSchema):
    # Converte os dados da passagem recebida para o modelo do banco de dados
    passagem_data = passagem.model_dump()
    passagem_model = PassagemModel(**passagem_data) 

    try:
        capacidade_voo = await db_session.execute(
            select(VooModel.capacidade_voo).where(VooModel.id == passagem.id_voo)
        )
        capacidade_voo = capacidade_voo.scalar()
        if capacidade_voo is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Esse voo não existe",
            )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar capacidade do voo",
        )

    result = await db_session.execute(
        select(func.count(PassagemModel.id)).where(
            PassagemModel.id_voo == passagem.id_voo
        )
    )
    count_passagem = result.scalar()

    assento_ocupado = await db_session.execute(
        select(PassagemModel).where(
            (PassagemModel.assento == passagem.assento)
            & (PassagemModel.id_voo == passagem.id_voo)
        )
    )
    if assento_ocupado.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Assento Ocupado"
        )

    if count_passagem >= capacidade_voo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limite máximo de passagens para este voo alcançado.",
        )

    db_session.add(passagem_model)
    try:
        await db_session.commit()
        return passagem_model
    except Exception:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha ao comprar passagem",
        )


@router.post('/buy_ticket',  response_model=PassagemSchema, summary='Buy ticket')
async def buy_ticket(
    user_id: UUID, 
    db_session: DatabaseSession, 
    passagem: PassagemSchema2, 
    current_user=Depends(verify_login_current)
):
    # Converte os dados da passagem recebida para o modelo do banco de dados
    passagem_data = passagem.model_dump()
    passagem_data["id"] = passagem_data.get("id", uuid4())
    passagem_model = PassagemModel(**passagem_data)
    # Validação do UUID do usuário
    try:
        user_id = UUID(str(user_id))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID. Must be a UUID.")

    # Verifica se o usuário está logado
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # Verifica se o usuário autenticado é o dono da passagem
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    # Processamento para diferentes companhias aéreas
    if passagem.companhia_aerea == "BrAilines":
        # Lógica de compra para BrasilPass (processamento local)
        try:
            capacidade_voo = await db_session.execute(
                select(VooModel.capacidade_voo).where(VooModel.id == passagem.id_voo).with_for_update()
            )
            capacidade_voo = capacidade_voo.scalar()
            if capacidade_voo is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esse voo não existe")
        except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao buscar capacidade do voo")

        result = await db_session.execute(
            select(func.count(PassagemModel.id)).where(PassagemModel.id_voo == passagem.id_voo)
        )
        count_passagem = result.scalar()

        assento_ocupado = await db_session.execute(
            select(PassagemModel).where(
                (PassagemModel.assento == passagem.assento) & 
                (PassagemModel.id_voo == passagem.id_voo)
            ).with_for_update()
        )
        if assento_ocupado.scalars().first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assento Ocupado")

        if count_passagem >= capacidade_voo:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limite máximo de passagens para este voo alcançado.")

        db_session.add(passagem_model)
        try:
            await db_session.commit()
            return passagem_model 
        except Exception:
            await db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao comprar passagem")

    elif passagem.companhia_aerea == "BrasilPass":
        return await attempt_buy_ticket_external(
            "http://localhost:8000/ticket/buy_ticket_no_login", 
            passagem_data, 
            str(user_id),
            db_session
        )

    elif passagem.companhia_aerea == "VoeBr":
        return await attempt_buy_ticket_external(
            "http://localhost:8002/ticket/buy_ticket_no_login", 
            passagem_data, 
            str(user_id),
            db_session
        )
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Companhia aérea inválida")

async def buy_ticket_external(url: str, passagem_data: dict, user_id: str, db_session):
    """
    Realiza uma requisição para uma companhia aérea externa.
    """
    # Converte qualquer UUID presente no dict em string
    passagem_data = {key: (str(value) if isinstance(value, UUID) else value) for key, value in passagem_data.items()}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                params={"user_id": user_id},
                json=passagem_data
            )
            response.raise_for_status()  # Lança exceção para status 4xx/5xx

            # Salva a passagem no banco local se a resposta for bem-sucedida
            passagem_model = PassagemModel(**passagem_data)
            db_session.add(passagem_model)
            await db_session.commit()  # Confirma a transação no banco

            # Retorna o objeto de resposta HTTP diretamente
            return passagem_model

        except httpx.RequestError as e:
            print(f"Erro ao comunicar com o servidor externo: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Falha ao comunicar com o servidor externo"
            )
        except httpx.HTTPStatusError as e:
            print(f"Erro HTTP do servidor externo: {e}")
            if e.response.status_code == 400:
                # Verifica o conteúdo da resposta para identificar "assento ocupado"
                try:
                    error_detail = e.response.json().get("detail", "").lower()
                    if "assento ocupado" in error_detail:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Erro ao completar a compra: assento ocupado"
                        )
                except Exception:
                    pass
                # Caso 400 não seja sobre o assento, levanta erro genérico
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao completar a compra: dados inválidos")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Erro do servidor externo"
            )

async def attempt_buy_ticket_external(url: str, data: dict, user_id: str, db_session, max_retries: int = 3, retry_delay: int = 2):
    attempt = 0
    while attempt < max_retries:
        try:
            response = await buy_ticket_external(url, data, user_id, db_session)
            # Se bem-sucedido (status 200), retorna a resposta
            if response:
                return response
        except HTTPException as e:
            # Interrompe imediatamente se a exceção for um erro 400
            if e.status_code == status.HTTP_400_BAD_REQUEST:
                raise e
            print(f"Erro ao tentar compra no servidor remoto, tentativa {attempt + 1} de {max_retries}: {e}")
        except Exception as e:
            # Captura outros erros, como problemas de rede, e tenta novamente
            print(f"Erro inesperado, tentativa {attempt + 1} de {max_retries}: {e}")
        
        attempt += 1
        if attempt < max_retries:  # Espera antes da nova tentativa apenas se ainda restarem tentativas
            await asyncio.sleep(retry_delay)
    
    # Se todas as tentativas falharem, reverte a compra local
    await rollback_local_purchase(db_session, data["id"])
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao completar a compra no servidor externo.")

async def rollback_local_purchase(db_session, ticket_id):
    try:
        result = await db_session.execute(
            select(PassagemModel).where(PassagemModel.id == ticket_id)
        )
        ticket = result.scalars().first()
        if ticket:
            await db_session.delete(ticket)
            await db_session.commit()
            print(f"Compra revertida para ticket ID: {ticket_id}")
    except Exception as e:
        await db_session.rollback()
        print(f"Erro ao reverter compra local: {e}")
      
@router.get("/public-tickets", response_model=PassagemSchemaList, summary="List public tickets")
async def list_public_tickets(user_id: UUID, db_session: DatabaseSession, limit: int = 15):
    # Valida o formato do UUID do usuário
    
    # Realiza a consulta apenas no banco de dados local
    try:
        # Filtra as passagens locais apenas pelo id do passageiro
        subquery_voo_ids = select(VooModel.id).subquery()

        # Query principal que filtra passagens com base no id do passageiro e em ids de voo válidos
        local_tickets_query = select(PassagemModel).where(
        PassagemModel.id_passageiro == user_id,
        PassagemModel.id_voo.in_(subquery_voo_ids)
        ).limit(limit)

        local_result = await db_session.execute(local_tickets_query)
        local_tickets = local_result.scalars().all()

        return {'tickets': local_tickets}

    except Exception as e:
        print(f"Erro ao listar passagens locais: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao listar passagens locais")
    
@router.get("/", response_model=PassagemSchemaList, summary="List tickets")
async def list(user_id: UUID, db_session: DatabaseSession, limit: int = 15, current_user=Depends(verify_login_current)):
    # Validações iniciais
    try:
        user_id = UUID(str(user_id))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID. Must be a UUID.")

    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    # Consulta as passagens locais do usuário
    try:
        # Subquery para obter os ids de voos que estão na tabela `VoosModel`
        subquery_voo_ids = select(VooModel.id).subquery()

        # Query principal que filtra passagens com base no id do passageiro e em ids de voo válidos
        local_tickets_query = select(PassagemModel).where(
            PassagemModel.id_passageiro == user_id,
            PassagemModel.id_voo.in_(subquery_voo_ids)
        ).limit(limit)
        
        local_result = await db_session.execute(local_tickets_query)
        local_tickets = local_result.scalars().all()


    except Exception as e:
        print(f"Erro ao listar passagens locais: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao listar passagens locais")

    # Endereços dos servidores remotos
    remote_server_urls = [
        f"http://127.0.0.1:8000/ticket/public-tickets?user_id={user_id}",
        f"http://127.0.0.1:8002/ticket/public-tickets?user_id={user_id}"
    ]

    # Função para fazer a requisição a cada servidor com tratamento de erro
    async def fetch_tickets(url):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                response.raise_for_status()
                
                # Acessa a chave 'tickets' do dicionário retornado
                tickets_data = response.json().get('tickets', [])
                
                return tickets_data  # Retorna a lista de passagens de cada servidor
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                print(f"Erro ao comunicar com {url}: {e}")
                return []  # Retorna uma lista vazia em caso de falha

# Busca passagens dos servidores remotos em paralelo (sem interferir no resultado local)
    remote_tickets_lists = await asyncio.gather(*(fetch_tickets(url) for url in remote_server_urls))
    combined_remote_tickets = [ticket for tickets in remote_tickets_lists for ticket in tickets]
    print(combined_remote_tickets)
    # Filtra as passagens remotas com base nos ids de voo das passagens locais
    if combined_remote_tickets:
        # Combina passagens locais e remotas válidas
        return {'tickets': local_tickets + combined_remote_tickets}
    
    # Retorna apenas passagens locais se não houver passagens remotas válidas
    return {'tickets': local_tickets}

  
    
@router.delete("/{passagem_id}", response_model=DeletePassagemResponse, summary="Delete ticket")
async def delete_ticket(
    db_session: DatabaseSession, 
    passagem_id: str, 
    current_user=Depends(verify_login_current)
):
    # Validação do UUID da passagem
    try:
        passagem_id = UUID(passagem_id)
    except ValueError:
        logger.error(f"ID inválido recebido: {passagem_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido. Deve ser um UUID.")
    
    # Verificação do usuário atual
    if current_user is None:
        logger.error("Usuário não encontrado.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    # Busca a passagem no banco de dados local
    try:
        result = await db_session.execute(
            select(PassagemModel).where(PassagemModel.id == passagem_id)
        )
        ticket = result.scalars().first()
    except Exception as e:
        logger.error(f"Erro ao buscar passagem: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao buscar passagem")
    
    if ticket is None:
        logger.warning(f"Passagem não encontrada para ID: {passagem_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Passagem não encontrada")
    
    # Verificação de permissão do usuário
    if ticket.id_passageiro != current_user.id:
        logger.warning(f"Permissão insuficiente para o usuário: {current_user.id} ao deletar a passagem {passagem_id}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente para deletar esta passagem")
    
    # Tenta deletar a passagem no banco de dados
    try:
        await db_session.delete(ticket)
        await db_session.commit()
    except Exception as e:
        await db_session.rollback()  # Reverte em caso de erro
        logger.error(f"Erro ao deletar a passagem do banco de dados: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao deletar a passagem do banco de dados")

    # Deleção no servidor externo se necessário
    if ticket.companhia_aerea != 'BrAirlines':
        external_response = None
        try:
            if ticket.companhia_aerea == "BrasilPass":
                external_response = await delete_ticket_external("http://127.0.0.1:8000/ticket/delete_nologin", passagem_id)
            elif ticket.companhia_aerea == "VoeBr":
                external_response = await delete_ticket_external("http://127.0.0.1:8002/ticket/delete_nologin", passagem_id)
            
            if external_response.status_code != 200:
                logger.error(f"Erro ao deletar passagem no servidor externo para ID: {passagem_id}")
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao deletar passagem no servidor externo")
        except Exception as e:
            logger.error(f"Erro ao comunicar com servidor externo: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao comunicar com servidor externo")

    logger.info(f"Passagem deletada com sucesso: {passagem_id}")
    return {"detail": "Passagem deletada com sucesso"}


async def delete_ticket_external(url: str, passagem_id: UUID):
    """Chama o servidor externo para deletar a passagem usando httpx."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{url}/{passagem_id}")
            return response
        except httpx.HTTPStatusError as exc:
            print(f"Erro ao chamar o servidor externo: {exc.response.status_code} - {exc.response.text}")
            return None
        except Exception as e:
            print(f"Erro ao chamar o servidor externo: {e}")
            return None


@router.delete(
    "/delete_nologin/{passagem_id}", response_model=DeletePassagemResponse, summary="Delete ticket"
)
async def delete_ticket(
    db_session: DatabaseSession,
    passagem_id: str,
):

    result = await db_session.execute(
        select(PassagemModel).where(
            PassagemModel.id == passagem_id
        )  # Usando o modelo Ticket aqui
    )

    ticket = result.scalars().first()
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Passagem não encontrada"
        )


    try:
        await db_session.delete(ticket)
        await db_session.commit()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar a passagem",
        )

    return {"detail": "Passagem deletada com sucesso"}