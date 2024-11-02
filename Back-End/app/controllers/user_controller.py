from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from app.schemas.user_schemas import UserSchema, UserSchemaPublic, UserSchemaList, DeleteUserResponse, TokenSchema
from app.utils.dependecies import DatabaseSession
from app.models.user_model import UserModel
from app.security.security import get_password_hash, verify_password, create_acess_token, verify_login_current
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
    
@router.get("/users", response_model=UserSchemaList)
async def read_user(db_session: DatabaseSession, limit: int = 15):
    
    try:
        result = await db_session.execute(select(UserModel).limit(limit))
        users = result.scalars().all()
        return {'users': users}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao listar usuários")
    
@router.get("/", response_model=UserSchemaPublic)
async def read_user(current_user = Depends(verify_login_current)):
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não está logado")
        return current_user

    
@router.delete("/{user_id}", response_model=DeleteUserResponse, summary="Delete User")
async def update_user(db_session: DatabaseSession, user_id: str, user: UserSchema,current_user = Depends(verify_login_current)):

    try:
        user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido. Deve ser um UUID.")
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    if current_user.id != user_id:
        print(f'{current_user.id} => {user_id}')
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions'
        )
    
    try:
        await db_session.delete(current_user)
        await db_session.commit()
    except :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao deletar o usuário")
    
    return {"detail": "Usuário deletado com sucesso"}

@router.put("/{user_id}", response_model=DeleteUserResponse,  summary="Update User")

async def update_user(db_session: DatabaseSession, user_id:str, user: UserSchema, current_user = Depends(verify_login_current)):
    
    try:
        user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido. Deve ser um UUID.")
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    if current_user.id != user_id:
        print(f'{current_user.id} => {user_id}')
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not enough permissions'
        )
    
    try:
        current_user.cpf = user.cpf
        current_user.nome = user.nome
        current_user.password = get_password_hash(user.password)
        current_user.username = user.username
        db_session.add(current_user)
        await db_session.commit()
        return {"detail": "Usuário atualizado com sucesso"}
    except :
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao atualizar o usuário")

