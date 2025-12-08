from sqlalchemy import Column, String
from app.dao.db import Base
from uuid import uuid4

class UserTable(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)