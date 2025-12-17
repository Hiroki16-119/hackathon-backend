from dotenv import load_dotenv
load_dotenv()  # ← 先に読み込む

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import products, openai_description
from app.routes import users, auth  # 追加
from app.routes import predict
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# ✅ CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://hackathon-frontend-delta-lilac.vercel.app",
        "https://hackathon-frontend-git-main-hiroki16-119s-projects.vercel.app",
        "https://hackathon-frontend-a94mh59lr-hiroki16-119s-projects.vercel.app"  # ← 追加
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ここで "static" ディレクトリを "/static" パスにマウント
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ ルート登録
app.include_router(products.router)
app.include_router(openai_description.router)
app.include_router(users.router)   # 追加
app.include_router(auth.router)    # 追加
app.include_router(predict.router)

@app.get("/")
def root():
    return {"message": "API is running 🚀"}
