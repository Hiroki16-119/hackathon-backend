from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from app.models.models import ProductCreate, ProductRead
from app.dao.product_dao import (
    get_all_products,
    get_product_by_id,
    create_product
)
from app.dao.db import get_db

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=List[ProductRead])
def get_products(db: Session = Depends(get_db)):
    return get_all_products(db)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: str, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("", response_model=ProductRead)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)
