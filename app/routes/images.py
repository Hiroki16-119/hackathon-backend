from fastapi import APIRouter
from app.utils.gcs import generate_upload_url

router = APIRouter()

@router.post("/upload-url")
async def get_upload_url(filename: str):
    """アップロード用の署名付きURLを生成"""
    return generate_upload_url(filename)