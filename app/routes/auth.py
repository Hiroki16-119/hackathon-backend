from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel

from app.dao.db import get_db
from app.dao.user_dao import get_user_by_email, create_user, get_user_by_id

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: Optional[str] = None  # フロントが送る password を受け取れるように
    name: Optional[str] = None      # 任意

@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    # 開発用: password は検証せず、存在しなければユーザー作成
    email = payload.email
    name = payload.name or email.split("@")[0] or "Unnamed"
    user = get_user_by_email(db, email)
    if not user:
        user = create_user(db, name=name, email=email)
    # 開発用簡易トークン（user.id）
    return {"token": user.id}

@router.get("/me")
def me(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    token = parts[1]
    user = get_user_by_id(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user