from typing import List
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session

from app.dao.db import get_db
from app.dao.user_dao import get_user_by_id, create_user
from app.dao.product_dao import get_products_by_seller, get_product_by_id
from app.dao.purchase_table import PurchaseTable
from app.models.models import UserRead, UserUpdate, ProductRead
from app.utils.firebase_auth import verify_firebase_token

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, db: Session = Depends(get_db)):
    u = get_user_by_id(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u

@router.patch("/{user_id}", response_model=UserRead)
def patch_user(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    authorization: str = Header(...)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="認証情報がありません")
    token = authorization.split()[1]
    decoded = verify_firebase_token(token)
    if decoded["uid"] != user_id:
        raise HTTPException(status_code=403, detail="他人の情報は編集できません")
    u = get_user_by_id(db, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    updates = payload.dict(exclude_unset=True)
    for k, v in updates.items():
        setattr(u, k, v)
    db.commit()
    db.refresh(u)
    return u

@router.get("/{user_id}/products", response_model=List[ProductRead])
def get_user_products(user_id: str, db: Session = Depends(get_db)):
    prods = get_products_by_seller(db, user_id)
    return prods

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

@router.post("/", response_model=UserRead)
def create_user_api(
    payload: dict,
    db: Session = Depends(get_db),
    authorization: str = Header(...)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="認証情報がありません")
    token = authorization.split()[1]
    decoded = verify_firebase_token(token)
    uid = decoded["uid"]
    email = decoded.get("email")
    name = payload.get("displayName") or decoded.get("name")
    user = get_user_by_id(db, uid)
    if user:
        return user
    return create_user(db, uid, name, email)