from sqlalchemy import Column, String
from app.dao.db import Base

class UserTable(Base):
    __tablename__ = "users"

    id = Column(String(128), primary_key=True, index=True)  # Firebaseのuidは長いので128文字程度
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=False, unique=True)