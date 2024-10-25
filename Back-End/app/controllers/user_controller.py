from fastapi import APIRouter, Body, status
from schemas.user_schemas import UserSchema

router = APIRouter()


@router.post(
    "/",
    summary="user",
    status_code=status.HTTP_200_OK,
)
def create_user(user: UserSchema): ...
