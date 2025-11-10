from fastapi import APIRouter, HTTPException
import uuid
from app.models import Product

router = APIRouter(prefix="/products", tags=["Products"])

products = []

@router.get("")
def get_products():
    return products

@router.get("/{product_id}")
def get_product(product_id: str):
    for p in products:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@router.post("")
def add_product(product: Product):
    product_dict = product.dict()
    product_dict["id"] = str(uuid.uuid4())
    products.append(product_dict)
    return product_dict
