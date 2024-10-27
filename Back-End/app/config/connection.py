from app.config.settings import Settings
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

settings = Settings()
engine = create_async_engine(settings.DATABASE_URL,echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session