from fastapi import APIRouter, Body, status
from schemas.user_schemas import UserSchema, UserSchemaPublic
from models.user_model import UserModel
from utils.dependecies import DatabaseSession

router = APIRouter()


@router.post(
    "/",
    summary="Create User",
    status_code=status.HTTP_201_CREATED,
    response_model=UserSchemaPublic,
)
async def create_user(db_session:DatabaseSession, user: UserSchema): 
    user = UserModel(**user.model_dump())
    db_session.add(user)
    await db_session.commit()
    return user

@router.put("/{user_id}", response_model=UserSchemaPublic,  summary="Update User")
def update_user(user_id:int, user: UserSchema):
    pass

@router.delete("/{user_id}", response_model=UserSchemaPublic,  summary="Delete User")
def update_user(user_id:int, user: UserSchema):
    pass