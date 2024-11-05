from typing import List, Optional
import unicodedata
from fastapi import APIRouter, Body, Depends, status, HTTPException
import httpx
from sqlalchemy.future import select
from app.schemas.voo_schemas import VooSchema, VooSchemaList
from app.utils.dependecies import DatabaseSession
from app.models.voo_model import VooModel
from app.security.security import get_password_hash, verify_login_current, verify_password, create_acess_token
from uuid import UUID

router = APIRouter()

@router.post(
    "/",
    summary="Create Voo",
    status_code=status.HTTP_201_CREATED,
    response_model=VooSchema,
)

async def create_voos(db_session: DatabaseSession, voo: VooSchema):
    voo_instance = VooModel(**voo.model_dump())
    voo_validate = await db_session.execute(
    select(VooModel)
    .filter_by(origem=voo_instance.origem, destino=voo_instance.destino)
)

    existing_voo = voo_validate.scalars().first()
    
    if existing_voo is None: 
        db_session.add(voo_instance)
        try:
            await db_session.commit()
            await db_session.refresh(voo_instance)
            return voo_instance
        except:
            await db_session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao criar o voo")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O voo já existe")

import random
from fastapi import APIRouter, HTTPException, status
from sqlalchemy.future import select
import httpx

router = APIRouter()

@router.get("/", response_model=VooSchemaList, summary="Listar Voos")
async def read_voos(db_session: DatabaseSession, limit: int = 15):
    try:
        # Obter voos locais
        result = await db_session.execute(select(VooModel).limit(limit))
        voos_locais = result.scalars().all()
        voos_remotos = []

        async with httpx.AsyncClient() as client:
            try:
                dados_B = await client.get("http://localhost:8000/voo/list_public")
                dados_B.raise_for_status()
                voos_remotos.extend(dados_B.json().get('voos', []))
            except (httpx.RequestError, httpx.HTTPStatusError):
                print("Erro ao comunicar com o Servidor B, continuando com os dados locais.")

            try:
                dados_C = await client.get("http://localhost:8001/list_public")
                dados_C.raise_for_status()
                voos_remotos.extend(dados_C.json().get('voos', []))
            except (httpx.RequestError, httpx.HTTPStatusError):
                print("Erro ao comunicar com o Servidor C, continuando com os dados locais.")

        # Combinar os voos locais e remotos
        todos_voos = voos_locais + voos_remotos

        # Embaralhar a lista de voos
        random.shuffle(todos_voos)

        return {'voos': todos_voos}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar voos: {str(e)}"
        )
     
      
async def fetch_voos_from_server(url: str, params: dict) -> List[dict]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            print(response.json())
            return response.json().get('voos', [])
        except (httpx.RequestError, httpx.HTTPStatusError) as e:
            print(f"Erro ao comunicar com {url}: {str(e)}")
            return []  
        
def format_location(location: str) -> str:
    location = location.strip()
    location = location.title()
    corrections = {
    "De": "de",
    "Do": "do",
    "Da": "da",
    "E": "e"
    # Adicione mais palavras que você deseja manter em minúsculas
    }
    for key, value in corrections.items():
        location = location.replace(key.title(), value)
    return location

@router.get("/find", response_model=VooSchemaList, summary="List Voos")
async def read_voos_origem_destino(db_session: DatabaseSession, origem: Optional[str] = None, destino: Optional[str] = None, voo_id: Optional[UUID] = None):  
    if origem and destino:
        origem = format_location(origem)
        destino = format_location(destino)
        
    try:
        # Verifica se o ID do voo foi fornecido
        if voo_id is not None:
            result = await db_session.execute(select(VooModel).where(VooModel.id == voo_id))
            voos = result.scalars().all()
        elif origem and destino:
            result = await db_session.execute(
                select(VooModel).where((VooModel.destino == destino) & (VooModel.origem == origem))
            )
            voos = result.scalars().all()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parâmetros insuficientes")

        # Busca voos remotos
        voos_remotos_B = await fetch_voos_from_server("http://localhost:8000/voo/find_public", {"origem": origem, "destino": destino})
        voos_remotos_C = await fetch_voos_from_server("http://localhost:8001/voo/find_public", {"origem": origem, "destino": destino})

        todos_voos = voos + voos_remotos_B + voos_remotos_C

        return {'voos': todos_voos}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao listar voos: {str(e)}") 

@router.get("/list_public", response_model=VooSchemaList, summary="List Voos")
async def read_voos(db_session: DatabaseSession, limit: int = 15):
    try:
        result = await db_session.execute(select(VooModel).limit(limit))
        voos = result.scalars().all()
        return {'voos': voos}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao listar voos") 
    

@router.get("/find_public", response_model=VooSchemaList, summary="List Voos")
async def read_voos_origem_destino(db_session: DatabaseSession, origem: Optional[str] = None, destino: Optional[str] = None, voo_id: Optional[UUID] = None):  
    if origem and destino:
        origem = format_location(origem)
        destino = format_location(destino)
        
    try:
        # Verifica se o ID do voo foi fornecido
        if voo_id is not None:
            result = await db_session.execute(select(VooModel).where(VooModel.id == voo_id))
            voos = result.scalars().all()
        elif origem and destino:
            result = await db_session.execute(
                select(VooModel).where((VooModel.destino == destino) & (VooModel.origem == origem))
            )
            voos = result.scalars().all()
            return {'voos': voos}
            
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Parâmetros insuficientes")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao listar voos: {str(e)}") 