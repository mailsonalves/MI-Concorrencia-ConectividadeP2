from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from app.utils.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID


class PassagemModel(Base):
    __tablename__ = 'passagens'
    __table_args__ = {'extend_existing': True}

    id_voo: Mapped[UUID] = mapped_column(UUID, nullable=False)
    id_passageiro: Mapped[UUID] = mapped_column(UUID, nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), nullable=False)
    companhia_aerea: Mapped[str] = mapped_column(String(50), nullable=False)
    assento: Mapped[str] = mapped_column(String(5), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)



