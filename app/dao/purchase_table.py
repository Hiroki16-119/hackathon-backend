from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.dao.db import Base

class PurchaseTable(Base):
    __tablename__ = "purchases"
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    product_id = Column(String(36), ForeignKey("products.id"), nullable=False)
    purchased_at = Column(DateTime, server_default=func.now())