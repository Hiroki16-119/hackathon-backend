from google.cloud import storage
from datetime import timedelta

def upload_image_to_gcs(file_obj, filename, bucket_name="uttc", url_ttl_days=7):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(file_obj)
    # 署名付きURLを生成（例：7日有効）
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(days=url_ttl_days),
        method="GET",
    )
    return url