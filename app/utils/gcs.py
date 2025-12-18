from google.cloud import storage
import google.auth
from datetime import timedelta

def upload_image_to_gcs(file_obj, filename, bucket_name="uttc", url_ttl_days=7):
    credentials, project = google.auth.default()

    client = storage.Client(credentials=credentials, project=project)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)

    blob.upload_from_file(file_obj)

    signing_sa = getattr(credentials, "service_account_email", None)
    if not signing_sa:
        raise RuntimeError("service_account_email が取得できません")

    # ← credentials を明示的に渡す
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(days=url_ttl_days),
        method="GET",
        credentials=credentials,  # ← これが必須
        service_account_email=signing_sa,
    )
    return url