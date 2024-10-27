from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, Boolean
from app.utils.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class VooModel(Base):
    __tablename__ = 'voos'

    origem: Mapped[str] = mapped_column(String(50), nullable=False)
    destino: Mapped[str] = mapped_column(String(50), nullable=False)
    vagas: Mapped[str] = mapped_column(String, nullable=False)  # Consider changing this to JSON if necessary
    disponibilidade: Mapped[bool] = mapped_column(Boolean, nullable=False)