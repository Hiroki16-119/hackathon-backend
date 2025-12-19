from google.cloud import storage
import google.auth
import uuid

def generate_upload_url(filename: str):
    """GCSへのアップロード用の公開URLを生成"""
    credentials, project = google.auth.default()
    
    client = storage.Client(credentials=credentials, project=project)
    bucket = client.bucket("uttc")
    
    # ユニークなファイル名を生成
    unique_filename = f"products/{uuid.uuid4()}.{filename.split('.')[-1]}"
    blob = bucket.blob(unique_filename)
    
    # 公開URL（バケットが公開設定なので署名不要）
    public_url = f"https://storage.googleapis.com/uttc/{unique_filename}"
    
    return {
        "filename": unique_filename,
        "public_url": public_url
    }