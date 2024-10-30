from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from app.schemas.user_schemas import TokenSchema
from app.utils.dependecies import DatabaseSession
from app.models.user_model import UserModel
from app.security.security import get_password_hash, verify_password, create_acess_token
from uuid import UUID

router = APIRouter()


@router.post('/token', response_model=TokenSchema)
async def login_for_token(db_session: DatabaseSession,form_data: OAuth2PasswordRequestForm = Depends()):
    user_validate = await db_session.execute(select(UserModel).filter_by(username=form_data.username))
    existing_user = user_validate.scalars().first()
    
    if not existing_user or not verify_password(form_data.password, existing_user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou senha incorreto")
        
    acess_token = create_acess_token(data_payload={'sub':existing_user.username})
    
    return {'access_token' : acess_token, 'token_type': 'Bearer'}