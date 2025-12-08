from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List
from sqlalchemy.orm import Session
from uuid import uuid4

from app.models.models import ProductCreate, ProductRead, ProductUpdate
from app.dao.product_dao import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)
from app.dao.db import get_db
from app.dao.purchase_table import PurchaseTable
from app.dao.user_dao import get_user_by_id

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

@router.patch("/{product_id}", response_model=ProductRead)
def patch_product(product_id: str, payload: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product(db, product_id, payload)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
def remove_product(product_id: str, db: Session = Depends(get_db)):
    ok = delete_product(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "deleted"}


@router.post("/{product_id}/purchase")
def purchase_product(
    product_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="認証情報がありません")
    user_id = authorization.split()[1]


    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    if product.is_purchased:
        raise HTTPException(status_code=400, detail="すでに購入済みです")
    if product.seller_id == user_id:
        raise HTTPException(status_code=400, detail="自分の商品は購入できません")

    # 商品を購入済みにする
    product.is_purchased = True
    db.add(product)

    # 購入履歴を追加
    purchase = PurchaseTable(
        id=str(uuid4()),
        user_id=user_id,
        product_id=product_id
    )
    db.add(purchase)
    db.commit()
    return {"detail": "購入が完了しました"}


@router.get("/{user_id}/purchases", response_model=List[ProductRead])
def get_user_purchases(user_id: str, db: Session = Depends(get_db)):
    # 購入履歴を取得
    purchases = db.query(PurchaseTable).filter(PurchaseTable.user_id == user_id).all()
    # 購入した商品の詳細を取得
    products = []
    for purchase in purchases:
        product = get_product_by_id(db, purchase.product_id)
        if product:
            products.append(product)
    return products