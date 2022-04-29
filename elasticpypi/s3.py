import boto3
from elasticpypi.config import config

BUCKET = config["bucket"]


def upload(filename, payload):
    client = boto3.client("s3")
    client.upload_fileobj(payload, BUCKET, filename)
