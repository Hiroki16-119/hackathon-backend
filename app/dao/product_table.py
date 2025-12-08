from sqlalchemy import Column, String, Integer, Text, Boolean
from app.dao.db import Base

class ProductTable(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)  # DB の正しいカラム
    user_hint = Column(String(500), nullable=True)

    # seller 情報（フロントから渡される）
    seller_id = Column(String(36), nullable=True, index=True)
    seller_name = Column(String(255), nullable=True)
    is_purchased = Column(Boolean, nullable=False, default=False)  # ← 追加
