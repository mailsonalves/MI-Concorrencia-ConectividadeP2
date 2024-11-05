from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from fastapi.security import OAuth2PasswordBearer
from zoneinfo import ZoneInfo

from sqlalchemy import select
from app.utils.dependecies import DatabaseSession
from jwt import decode, encode
from datetime import datetime, timedelta
from app.schemas.user_schemas import TokenSchema, UserSchema
from app.models.user_model import UserModel
from app.config.settings import Settings

pwd = PasswordHash.recommended()
ouath2_schema = OAuth2PasswordBearer(tokenUrl='auth/token')
settings = Settings()



def get_password_hash(password: str):
    return pwd.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd.verify(plain_password, hashed_password)

def create_acess_token(data_payload: dict):
    to_encode_copy = data_payload.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=settings.TOKEN_EXPIRE_MIN)
    
    to_encode_copy.update({'exp':expire})
    encode_jwt = encode(to_encode_copy,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    
    return encode_jwt
    
async def verify_login_current(db_session: DatabaseSession , token: str = Depends(ouath2_schema)):
    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = UserModel(username=username)

    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


    user_validate = await db_session.execute(select(UserModel).filter_by(username=token_data.username))
    user = user_validate.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user