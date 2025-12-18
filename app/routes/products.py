from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, File, Form
from typing import List
from sqlalchemy.orm import Session
from uuid import uuid4
import os
import shutil

from app.models.models import ProductRead, ProductUpdate
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
from app.utils.firebase_auth import verify_firebase_token
from app.utils.gcs import upload_image_to_gcs  # 追加

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
async def add_product(
    name: str = Form(...),
    price: int = Form(...),
    category: str = Form(...),
    description: str = Form(""),
    image: UploadFile = File(None),
    imageUrl: str = Form(""),
    user_hint: str = Form(""),
    db: Session = Depends(get_db),
    authorization: str = Header(...)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="認証情報がありません")
    token = authorization.split()[1]
    decoded = verify_firebase_token(token)
    user_id = decoded["uid"]

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")

    # 画像ファイルがあればGCSにアップロードし、そのURLをimage_urlに
    image_url = imageUrl
    if image:
        ext = os.path.splitext(image.filename)[1]
        img_id = str(uuid4())
        filename = f"products/{img_id}{ext}"
        image_url = upload_image_to_gcs(image.file, filename)  # GCSアップロード

    # DB保存
    from app.models.models import ProductCreate
    product_data = {
        "name": name,
        "price": price,
        "category": category,
        "description": description,
        "image_url": image_url,
        "user_hint": user_hint,
        "seller_id": user_id,
        "seller_name": user.name,
    }
    product = ProductCreate(**product_data)
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
    authorization: str = Header(...)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="認証情報がありません")
    token = authorization.split()[1]
    decoded = verify_firebase_token(token)
    user_id = decoded["uid"]

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


