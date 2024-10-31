from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from app.schemas.user_schemas import TokenSchema, UserSchema
from app.utils.dependecies import DatabaseSession
from app.models.user_model import UserModel
from app.security.security import get_password_hash, verify_login_current, verify_password, create_acess_token
from uuid import UUID

router = APIRouter()

@router.post('/', response_model=TokenSchema, summary='Buy ticket')
async def login_for_token(db_session: DatabaseSession, user_id:str, user: UserSchema, current_user = Depends(verify_login_current)):
    ...