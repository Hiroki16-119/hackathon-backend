from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import products, openai_description

load_dotenv()

app = FastAPI()

# ✅ CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ルート登録
app.include_router(products.router)
app.include_router(openai_description.router)

@app.get("/")
def root():
    return {"message": "API is running 🚀"}
