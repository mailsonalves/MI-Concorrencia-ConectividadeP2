from datetime import datetime
from typing import List
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from app.utils.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    

