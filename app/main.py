from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routes import products, openai_description, users, auth, predict, images

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://hackathon-frontend-delta-lilac.vercel.app",
        "https://hackathon-frontend-git-main-hiroki16-119s-projects.vercel.app",
        "https://hackathon-frontend-a94mh59lr-hiroki16-119s-projects.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# ルート登録（prefix は main.py で指定）
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(images.router, prefix="/images", tags=["images"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(openai_description.router, prefix="/generate_description", tags=["AI Description"]) 
app.include_router(auth.router, prefix="/auth", tags=["auth"])  
app.include_router(predict.router)  

@app.get("/")
def root():
    return {"message": "API is running 🚀"}
