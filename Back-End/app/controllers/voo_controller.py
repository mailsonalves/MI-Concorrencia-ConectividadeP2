from fastapi import APIRouter, Body, Depends, status, HTTPException
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

async def create_passagem(db_session: DatabaseSession, voo: VooSchema):
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

@router.get("/", response_model=VooSchemaList, summary="List Voos")
async def read_user(db_session: DatabaseSession, limit: int = 15):
    try:
        result = await db_session.execute(select(VooModel).limit(limit))
        voos = result.scalars().all()
        return {'voos': voos}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao listar voos")       