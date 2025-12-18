from google.cloud import storage
from google.auth.transport import requests as auth_requests
from google.auth import iam
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
    
    service_account_email = getattr(credentials, "service_account_email", None)
    if not service_account_email:
        raise RuntimeError("service_account_email が取得できません")
    
    # 秘密鍵がない場合は IAM Signer を使用
    if not hasattr(credentials, "signer"):
        signing_credentials = iam.Signer(
            auth_requests.Request(),
            credentials,
            service_account_email
        )
    else:
        signing_credentials = credentials
    
    expiration = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # アップロード用の署名付きURL（PUT メソッド）
    upload_url = blob.generate_signed_url(
        version="v4",
        expiration=expiration,
        method="PUT",
        credentials=signing_credentials,
        service_account_email=service_account_email,
    )
    
    # 公開用URL（7日間有効な署名付き読み取りURL）
    read_url = blob.generate_signed_url(
        version="v4",
        expiration=datetime.now(timezone.utc) + timedelta(days=7),
        method="GET",
        credentials=signing_credentials,
        service_account_email=service_account_email,
    )
    
    return {
        "upload_url": upload_url,
        "read_url": read_url,
        "filename": unique_filename
    }