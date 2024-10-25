from utils.schemas import BaseModel
from typing import Annotated
from pydantic import Field

class UserSchema(BaseModel):
    username: Annotated[str, Field(
        description='username do usuário',
        examples=['user_1'],
        max_length=50
    )]
    
    nome: Annotated[str, Field(
        description='Nome do usuário',
        examples=['João'],
        max_length=50
    )]
    
    cpf: Annotated[str, Field(
        description='CPF do usuário',
        examples=['123.456.789-00'],
        max_length=14
    )]
    
    password: Annotated[str, Field(
        description='password do usuário',
        examples=['1234'],
        max_length=14
    )]
    
    