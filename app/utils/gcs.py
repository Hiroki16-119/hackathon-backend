from google.cloud import storage
from google.auth.transport import requests
from google.auth import iam
from google.auth import compute_engine
import google.auth
from datetime import timedelta, datetime, timezone
import urllib.parse

def upload_image_to_gcs(file_obj, filename, bucket_name="uttc", url_ttl_days=7):
    credentials, project = google.auth.default()

    client = storage.Client(credentials=credentials, project=project)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)

    blob.upload_from_file(file_obj)

    # Compute Engine credentials の場合は IAM Credentials API を使う
    if isinstance(credentials, compute_engine.Credentials):
        # IAM Credentials API を使って署名
        signing_credentials = iam.Signer(
            requests.Request(),
            credentials,
            credentials.service_account_email
        )
        
        expiration = datetime.now(timezone.utc) + timedelta(days=url_ttl_days)
        
        url = blob.generate_signed_url(
            version="v4",
            expiration=expiration,
            method="GET",
            credentials=signing_credentials,
            service_account_email=credentials.service_account_email,
        )
    else:
        # サービスアカウント JSON を使っている場合
        signing_sa = getattr(credentials, "service_account_email", None)
        if not signing_sa:
            raise RuntimeError("service_account_email が取得できません")
        
        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(days=url_ttl_days),
            method="GET",
            credentials=credentials,
            service_account_email=signing_sa,
        )
    
    return url