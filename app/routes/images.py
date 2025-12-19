from fastapi import APIRouter, File, UploadFile, HTTPException
from google.cloud import storage
import google.auth
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """画像をGCSにアップロード"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="画像ファイルのみアップロード可能です")
    
    if file.size and file.size > 12 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="ファイルサイズは12MB以下にしてください")
    
    # Google Cloud Storage クライアント
    credentials, project = google.auth.default()
    client = storage.Client(credentials=credentials, project=project)
    bucket = client.bucket("uttc")
    
    # ユニークなファイル名を生成
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    unique_filename = f"products/{uuid.uuid4()}.{ext}"
    blob = bucket.blob(unique_filename)
    
    # GCSにアップロード
    blob.upload_from_file(file.file, content_type=file.content_type)
    
    # 公開URL
    public_url = f"https://storage.googleapis.com/uttc/{unique_filename}"
    
    return {
        "filename": unique_filename,
        "url": public_url
    }