from datetime import datetime
from typing import List
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey, Boolean
from app.utils.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class VooModel(Base):
    __tablename__ = 'voos'
    __table_args__ = {'extend_existing': True}
    origem: Mapped[str] = mapped_column(String(50), nullable=False)
    destino: Mapped[str] = mapped_column(String(50), nullable=False)
    capacidade_voo: Mapped[bool] = mapped_column(Integer, nullable=False)
    companhia_aerea: Mapped[bool] = mapped_column(String, nullable=False)
    preco: Mapped[int] = mapped_column(Integer, nullable=True)
    imagem_companhia: Mapped[bool] = mapped_column(String, nullable=True)
    
