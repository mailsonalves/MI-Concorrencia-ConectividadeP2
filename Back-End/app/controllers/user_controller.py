from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from app.schemas.user_schemas import UserSchema, UserSchemaPublic, UserSchemaList, DeleteUserResponse, TokenSchema
from app.utils.dependecies import DatabaseSession
from app.models.user_model import UserModel
from app.security.security import get_password_hash, verify_password, create_acess_token, verify_login
from uuid import UUID

router = APIRouter()


@router.post(
    "/",
    summary="Create User",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchemaPublic,
)


async def create_user(db_session: DatabaseSession, user: UserSchema): 
    user_instance = UserModel(**user.model_dump())
    user_validate = await db_session.execute(select(UserModel).filter_by(username=user_instance.username))
    existing_user = user_validate.scalars().first()
    
    if existing_user is None: 
        user_instance.password = get_password_hash(user_instance.password)
        print(user_instance.password)
        db_session.add(user_instance)
        try:
            await db_session.commit()
            await db_session.refresh(user_instance)
            return user_instance
        except:
            await db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao criar o usuário")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O usuário já existe")
    
@router.get("/", response_model=UserSchemaList)
async def read_user(db_session: DatabaseSession, limit: int = 15):
    
    try:
        result = await db_session.execute(select(UserModel).limit(limit))
        users = result.scalars().all()
        return {'users': users}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao listar usuários")
    
@router.delete("/{user_id}", response_model=DeleteUserResponse, summary="Delete User")
async def update_user(db_session: DatabaseSession, user_id: str, user: UserSchema):

    try:
        user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido. Deve ser um UUID.")
    

    user_validate = await db_session.execute(select(UserModel).filter_by(id=user_id))
    user = user_validate.scalars().first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
  
    await db_session.delete(user)
    await db_session.commit()
    
    return {"detail": "Usuário deletado com sucesso"}

@router.put("/{user_id}", response_model=DeleteUserResponse,  summary="Update User")
async def update_user(db_session: DatabaseSession, user_id:str, user: UserSchema, current_user = Depends(verify_login)):
    try:
        user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido. Deve ser um UUID.")
    
    user_validate = await db_session.execute(select(UserModel).filter_by(id=user_id))
    user_db = user_validate.scalars().first()
    
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    
    try:
        user_db.cpf = user.cpf
        user_db.nome = user.nome
        user_db.password = get_password_hash(user.password)
        user_db.username = user.username
        db_session.add(user_db)
        await db_session.commit()
        return {"detail": "Usuário atualizado com sucesso"}
    except :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao atualizar o usuário")

@router.post('/token', response_model=TokenSchema)
async def login_for_token(db_session: DatabaseSession,form_data: OAuth2PasswordRequestForm = Depends()):
    user_validate = await db_session.execute(select(UserModel).filter_by(username=form_data.username))
    existing_user = user_validate.scalars().first()
    
    if not existing_user or not verify_password(form_data.password, existing_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou senha incorreto")
        
    acess_token = create_acess_token(data_payload={'sub':existing_user.username})
    
    return {'access_token' : acess_token, 'token_type': 'Bearer'}