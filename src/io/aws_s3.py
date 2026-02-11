# src/io/aws_s3.py

from pathlib import Path
import sys
import os

import boto3
from dotenv import load_dotenv, find_dotenv

from src.config import RAW_DIR, OUTPUT_DIR

# Chargement des variables d'environnement (.env)
load_dotenv(find_dotenv(), override=True)

API_KEY_S3 = os.getenv("API_KEY_S3")
API_SECRET_KEY_S3 = os.getenv("API_SECRET_KEY_S3")
AWS_REGION = "eu-west-3"
BUCKET_NAME = "dsfs36-bucket-01"


def get_s3_resource():
    """Crée une ressource S3 boto3 à partir des clés du fiochier .env."""
    session = boto3.Session(
        aws_access_key_id=API_KEY_S3,
        aws_secret_access_key=API_SECRET_KEY_S3,
        region_name=AWS_REGION,
    )
    return session.resource("s3")


def upload_file(local_path: Path, s3_key: str):
    """Upload un fichier local vers S3 sous la clé s3_key."""
    s3 = get_s3_resource()
    bucket = s3.Bucket(BUCKET_NAME)
    bucket.upload_file(str(local_path), s3_key)
    print(f"Upload {local_path} -> s3://{BUCKET_NAME}/{s3_key}")


def upload_raw_folder(prefix: str = "raw/"):
    """Upload tous les CSV du dossier data/raw vers S3."""
    for path in RAW_DIR.glob("*.csv"):
        s3_key = f"{prefix}{path.name}"
        upload_file(path, s3_key)


def upload_outputs_folder(prefix: str = "outputs/"):
    """Upload tous les CSV du dossier data/outputs vers S3."""
    for path in OUTPUT_DIR.glob("*.csv"):
        s3_key = f"{prefix}{path.name}"
        upload_file(path, s3_key)


def upload_all():
    """Upload raw + outputs."""
    upload_raw_folder()
    upload_outputs_folder()


if __name__ == "__main__":
    upload_all()
