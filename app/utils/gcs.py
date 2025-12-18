from google.cloud import storage

def upload_image_to_gcs(file_obj, filename, bucket_name="uttc"):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(filename)
    blob.upload_from_file(file_obj)
    blob.make_public()
    return blob.public_url