from datetime import datetime
from sqlalchemy import Integer, String, Float, DateTime, ForeignKey
from app.utils.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserModel(Base):
    __tablename__ = 'users'
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), unique=True,  nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)

