from fastapi import APIRouter, HTTPException
from typing import List
from app.models import Product

router = APIRouter(prefix="/products", tags=["Products"])

products = []

@router.get("", response_model=List[Product])
def get_products():
    return products

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str):
    for p in products:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("", response_model=Product)
def add_product(product: Product):
    products.append(product)
    return product
