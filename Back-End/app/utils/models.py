from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from uuid import uuid4

Base = declarative_base()

