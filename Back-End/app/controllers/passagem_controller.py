from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.future import select
from app.schemas.passagem_schemas import PassagemSchema, PassagemSchemaList
from app.models.voo_model import VooModel
from app.utils.dependecies import DatabaseSession
from app.models.passagem_model import PassagemModel
from app.security.security import get_password_hash, verify_login_current, verify_password, create_acess_token
from uuid import UUID

router = APIRouter()

@router.post('/buy_ticket', response_model=PassagemSchema, summary='Buy ticket')
async def buy_ticket(user_id: UUID, db_session: DatabaseSession, passagem: PassagemSchema, current_user=Depends(verify_login_current)):
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
        assento_validate = await db_session.execute(select(PassagemModel).filter_by(assento=passagem.assento))
        assento_user = assento_validate.scalars().first()
        
        if assento_user:
         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assento Ocupado")
            
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao selecionar assento passagem")
        
        
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
async def read_user(user_id: UUID, db_session: DatabaseSession, limit: int = 15, current_user=Depends(verify_login_current)):
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
    
    