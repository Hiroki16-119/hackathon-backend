from google.cloud import storage
import google.auth
from google.oauth2 import service_account
import os
from datetime import timedelta

def upload_image_to_gcs(file_obj, filename, bucket_name="uttc", url_ttl_days=7):
    # ADC を取得（Cloud Run では自動、ローカルでは env のサービスアカウント JSON を期待）
    credentials, project = google.auth.default()


    client = storage.Client(credentials=credentials, project=project)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(file_obj)

    # 署名に使うサービスアカウントメールを決定
    signing_sa = os.getenv("SIGNING_SERVICE_ACCOUNT") or getattr(credentials, "service_account_email", None) or getattr(credentials, "signer_email", None)
    if not signing_sa:
        raise RuntimeError("署名用サービスアカウントが見つかりません。ローカルなら GOOGLE_APPLICATION_CREDENTIALS をサービスアカウントJSONに設定してください。")

    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(days=url_ttl_days),
        method="GET",
        credentials=credentials,
        service_account_email=signing_sa,
    )
    return url