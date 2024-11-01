from app.utils.schemas import BaseModel
from typing import Annotated, List
from pydantic import Field
from pydantic import UUID4, Field

class PassagemSchema(BaseModel):
    id_voo: Annotated[UUID4, Field(
        description='ID do voo',
        examples=['477a3d30-b1e5-482d-966f-75339a9328b2'],
    )]
    
    id_passageiro: Annotated[UUID4, Field(
        description='Id do passageiro',
        examples=['4c6144a2-91ff-428c-91d3-5eca7b52d2bf'],
    )]
    
    cpf: Annotated[str, Field(
        description='CPF do usuário',
        examples=['123.456.789-00'],
    )]
    
    assento: Annotated[str, Field(
        description='Assento do usuário',
        examples=['A1'],
    )]
    companhia_aerea: Annotated[str, Field(
        description='Companhia Aerea',
        examples=['Companhia A'],
    )]

class PassagemSchemaList(BaseModel):
    tickets: List[PassagemSchema]