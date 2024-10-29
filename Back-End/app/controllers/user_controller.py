from fastapi import APIRouter, Body, status, HTTPException
from sqlalchemy.future import select
from app.schemas.user_schemas import UserSchema, UserSchemaPublic, UserSchemaList, DeleteUserResponse
from app.utils.dependecies import DatabaseSession
from app.models.user_model import UserModel
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

@router.put("/{user_id}", response_model=UserSchemaPublic,  summary="Update User")
def update_user(user_id:int, user: UserSchema):
    pass