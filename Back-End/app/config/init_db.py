from app.config.connection import engine
from asyncio import run
from app.utils.models import Base
from app.models.passagem_model import PassagemModel  # Importando os modelos
from app.models.voo_model import VooModel
from app.models.user_model import UserModel


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    run(create_database())
