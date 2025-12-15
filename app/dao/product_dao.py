from sqlalchemy.orm import Session
from app.dao.product_table import ProductTable
from app.models.models import ProductCreate, ProductRead, ProductUpdate
from uuid import uuid4

def get_all_products(db: Session):
    return db.query(ProductTable).all()

def get_product_by_id(db: Session, product_id: str):
    return db.query(ProductTable).filter(ProductTable.id == product_id).first()

def get_products_by_seller(db: Session, seller_id: str):
    return db.query(ProductTable).filter(ProductTable.seller_id == seller_id).all()

def create_product(db: Session, product: ProductCreate):
    # Pydantic の field 名が image_url か imageUrl のどちらでも受け取れるようにする
    image = getattr(product, "image_url", None) or getattr(product, "imageUrl", None)
    db_product = ProductTable(
        id=str(uuid4()),
        name=product.name,
        price=product.price,
        category=product.category,
        description=product.description,
        image_url=image,
        user_hint=product.user_hint,
        seller_id=product.seller_id,
        seller_name=product.seller_name
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: str, payload: ProductUpdate):
    p = get_product_by_id(db, product_id)
    if not p:
        return None
    data = payload.dict(exclude_unset=True, by_alias=False)
    # imageUrl alias を考慮
    if "imageUrl" in payload.__dict__:
        data["image_url"] = getattr(payload, "imageUrl", None)
    # map fields
    for k, v in data.items():
        if hasattr(p, k):
            setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

def delete_product(db: Session, product_id: str):
    p = get_product_by_id(db, product_id)
    if not p:
        return False
    db.delete(p)
    db.commit()
    return True