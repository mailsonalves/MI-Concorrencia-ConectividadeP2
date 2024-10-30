from pwdlib import PasswordHash
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from zoneinfo import ZoneInfo
from app.utils.dependecies import DatabaseSession
from jwt import decode, encode
from datetime import datetime, timedelta

pwd = PasswordHash.recommended()
ouath2_schema = OAuth2PasswordBearer(tokenUrl='token')
SECRET_KEY = ''
ALGORITHM = 'HS256'
TOKEN_EXPIRE_MIN = 30


def get_password_hash(password: str):
    return pwd.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd.verify(plain_password, hashed_password)

def create_acess_token(data_payload: dict):
    to_encode_copy = data_payload.copy
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(min=TOKEN_EXPIRE_MIN)
    
    to_encode_copy.update({'exp':expire})
    encode_jwt = encode(to_encode_copy,SECRET_KEY,algorithm=ALGORITHM)
    
    return encode_jwt
    
def verify_login(db_session: DatabaseSession, token: str = Depends(ouath2_schema)):
    payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get('sub')