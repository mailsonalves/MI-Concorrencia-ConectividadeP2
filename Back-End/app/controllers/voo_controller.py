from fastapi import APIRouter, Body, status, HTTPException
from sqlalchemy.future import select
from app.schemas.voo_schemas import VooSchema
from app.utils.dependecies import DatabaseSession
from app.models.voo_model import VooModel
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
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao criar o usuário")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O usuário já existe")