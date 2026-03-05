import os
import uuid
from google.cloud import storage
from fastapi import UploadFile

GCS_BUCKET_PRODUCTS = os.getenv("GCS_BUCKET_PRODUCTS")
GCS_BUCKET_PROFILES = os.getenv("GCS_BUCKET_PROFILES")

client = storage.Client()


def _upload_file(bucket_name: str, file: UploadFile, folder: str = "") -> str:
    bucket = client.bucket(bucket_name)
    extension = file.filename.split(".")[-1]
    filename = f"{folder}/{uuid.uuid4()}.{extension}" if folder else f"{uuid.uuid4()}.{extension}"
    blob = bucket.blob(filename)
    blob.upload_from_file(file.file, content_type=file.content_type)
    return blob.public_url


def upload_product_image(file: UploadFile, product_id: int) -> str:
    return _upload_file(GCS_BUCKET_PRODUCTS, file, folder=str(product_id))


def upload_profile_image(file: UploadFile, user_id: int) -> str:
    return _upload_file(GCS_BUCKET_PROFILES, file, folder=str(user_id))


def delete_file(bucket_name: str, public_url: str):
    prefix = f"https://storage.googleapis.com/{bucket_name}/"
    blob_name = public_url.replace(prefix, "")
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()


def delete_product_image(public_url: str):
    delete_file(GCS_BUCKET_PRODUCTS, public_url)


def delete_profile_image(public_url: str):
    delete_file(GCS_BUCKET_PROFILES, public_url)