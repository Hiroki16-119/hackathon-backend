from google.cloud import storage
import google.auth
from datetime import timedelta, datetime, timezone
import uuid

def generate_upload_url(filename: str):
    """GCSへのアップロード用署名付きURLを生成"""
    credentials, project = google.auth.default()
    
    client = storage.Client(credentials=credentials, project=project)
    bucket = client.bucket("uttc")
    
    # ユニークなファイル名を生成
    unique_filename = f"products/{uuid.uuid4()}.{filename.split('.')[-1]}"
    blob = bucket.blob(unique_filename)
    
    expiration = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # アップロード用の署名付きURL（PUT メソッド）← 秘密鍵不要
    upload_url = blob.generate_signed_url(
        version="v4",
        expiration=expiration,
        method="PUT",
    )
    
    # 公開URL（署名なし）← GCS バケットを公開設定にする
    public_url = f"https://storage.googleapis.com/uttc/{unique_filename}"
    
    return {
        "upload_url": upload_url,
        "read_url": public_url,  # ← 署名なし公開URL
        "filename": unique_filename
    }