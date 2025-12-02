import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PWD = os.getenv("MYSQL_PWD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")

# GCP 本番：MYSQL_HOST が '/cloudsql/' で始まる場合
if MYSQL_HOST.startswith("/cloudsql/"):
    DATABASE_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}@/{MYSQL_DATABASE}"
        f"?unix_socket={MYSQL_HOST}"
    )
# ローカル：通常の TCP 接続
else:
    DATABASE_URL = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PWD}"
        f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
    )

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args={"charset": "utf8mb4"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# DBセッションを生成して yield する依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
