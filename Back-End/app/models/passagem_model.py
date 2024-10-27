from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from app.utils.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class PassagemModel(Base):
    __tablename__ = 'passagens'
    id_voo: Mapped[int] = mapped_column(Integer, ForeignKey('voos.id'))
    id_passageiro: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'))
    cpf: Mapped[str] = mapped_column(String(14), nullable=False)
    assento: Mapped[str] = mapped_column(String(5), nullable=True)
    usuario: Mapped['users'] = relationship("User", back_populates="passagens")
    voo: Mapped['Voo'] = relationship("Voo")