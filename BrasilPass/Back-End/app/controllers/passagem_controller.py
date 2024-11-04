from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.passagem_schemas import PassagemSchema, PassagemSchemaList, DeletePassagemResponse, PassagemSchema2
from app.models.voo_model import VooModel
from app.utils.dependecies import DatabaseSession
from app.models.passagem_model import PassagemModel
from app.security.security import get_password_hash, verify_login_current, verify_password, create_acess_token
from uuid import UUID

router = APIRouter()



@router.post('/buy_ticket', response_model=PassagemSchema, summary='Buy ticket')
async def buy_ticket(user_id: UUID, db_session: DatabaseSession, passagem: PassagemSchema2, current_user=Depends(verify_login_current)):
    passagem = PassagemModel(**passagem.model_dump())
    try:

        user_id = UUID(str(user_id))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID. Must be a UUID.")

    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    try:
        capacidade_voo = await db_session.execute(
            select(VooModel.capacidade_voo)
            .where(VooModel.id == passagem.id_voo)
        )
        capacidade_voo = capacidade_voo.scalar()
    except:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Esse voo não existe")

    result = await db_session.execute(
        select(func.count(PassagemModel.id))
        .where(PassagemModel.id_voo == passagem.id_voo)
    )
    
    try:
        # Verifica se o assento já está ocupado
        assento_validate = await db_session.execute(
            select(PassagemModel).where(
                (PassagemModel.assento == passagem.assento) & 
                (PassagemModel.id_voo == passagem.id_voo)
            )
        )
        assento_ocupado = assento_validate.scalars().first()
        
        if assento_ocupado:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Assento Ocupado"
            )

    except SQLAlchemyError as e:
        # Exibe o erro no log para diagnóstico
        print(f"Erro ao verificar assento: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Falha ao selecionar assento passagem"
        )
        
        
    count_passagem = result.scalar()
    print(count_passagem)

    if count_passagem >= capacidade_voo:  # Limite máximo de 2 passagens por voo
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Limite máximo de passagens para este voo alcançado.")
    
    db_session.add(passagem)
    try:
        await db_session.commit()
        return passagem 
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao comprar passagem")
            
      
@router.get("/", response_model=PassagemSchemaList, summary="List tickets")
async def delete_passagem(user_id: UUID, db_session: DatabaseSession, limit: int = 15, current_user=Depends(verify_login_current)):
    try:
        user_id = UUID(str(user_id))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID. Must be a UUID.")

    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    try:
        result = await db_session.execute(select(PassagemModel).where(PassagemModel.id_passageiro == current_user.id).limit(limit))
        tickets = result.scalars().all()
        return {'tickets': tickets}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao listar usuários")       
    
@router.delete("/{passagem_id}", response_model=DeletePassagemResponse, summary="Delete ticket")
async def delete_ticket(db_session: DatabaseSession, passagem_id: str, current_user=Depends(verify_login_current)):
    
    try:
        passagem_id = UUID(passagem_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido. Deve ser um UUID.")
    
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    result = await db_session.execute(
        select(PassagemModel).where(PassagemModel.id == passagem_id)  # Usando o modelo Ticket aqui
    )
    
    ticket = result.scalars().first()  
    if ticket is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Passagem não encontrada")
    
    # Verificar se o usuário tem permissão para deletar a passagem (ajuste conforme necessário)
    if ticket.id_passageiro != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente para deletar esta passagem")
    
    try:
        await db_session.delete(ticket)
        await db_session.commit()
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao deletar a passagem")
    
    return {"detail": "Passagem deletada com sucesso"}
