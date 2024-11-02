from app.utils.schemas import BaseModel
from typing import Annotated, List
from pydantic import Field
from pydantic import UUID4, Field

class VooSchema(BaseModel):
    id: Annotated[UUID4, Field(
        description='ID único do voo',
    )]
    origem: Annotated[str, Field(
        description='Origem do voo',
        examples=['Salvador'],
        max_length=50
    )]
    
    destino: Annotated[str, Field(
        description='destino do voo',
        examples=['São Paulo'],
        max_length=50
    )]
    
    capacidade_voo: Annotated[int, Field(
        description='Capacidade do voo',
        examples=['2'],
    )]
    
    companhia_aerea: Annotated[str, Field(
        description='Companhia Aerea',
        examples=['Companhia A'],
    )]
    preco: Annotated[int, Field(
        description='Companhia Aerea',
        examples=['100'],
    )]
    imagem_companhia: Annotated[str, Field(
        description='Companhia Aerea',
        examples=['Companhia A'],
    )]

class VooSchemaList(BaseModel):
    voos: List[VooSchema]