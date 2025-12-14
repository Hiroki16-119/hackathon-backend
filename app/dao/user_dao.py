from sqlalchemy.orm import Session
from app.dao.user_table import UserTable

def get_user_by_id(db: Session, user_id: str):
    return db.query(UserTable).filter(UserTable.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(UserTable).filter(UserTable.email == email).first()

def create_user(db: Session, uid: str, name: str | None, email: str):
    # name が None の場合は email のローカル部をデフォルト名にする
    default_name = name or (email.split("@")[0] if "@" in email else "Unnamed")
    u = UserTable(id=uid, name=default_name, email=email)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u