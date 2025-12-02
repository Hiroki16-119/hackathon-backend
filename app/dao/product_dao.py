from sqlalchemy.orm import Session
from app.dao.product_table import ProductTable
from app.models.models import ProductCreate, ProductRead
from uuid import uuid4

def get_all_products(db: Session):
    return db.query(ProductTable).all()

def get_product_by_id(db: Session, product_id: str):
    return db.query(ProductTable).filter(ProductTable.id == product_id).first()

def create_product(db: Session, product: ProductCreate):
    db_product = ProductTable(
        id=str(uuid4()),
        name=product.name,
        price=product.price,
        description=product.description,
        image_url=product.imageUrl,   # ← Pydantic(camel) → DB(snake) 変換
        user_hint=product.user_hint
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product