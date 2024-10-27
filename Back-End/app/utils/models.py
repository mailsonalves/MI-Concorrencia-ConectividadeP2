from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import UUID
from uuid import uuid4

class Base(DeclarativeBase):
    __abstract__ = True  
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
