"""
Client for AWS S3.
"""
import hashlib
from io import BytesIO

import boto3


class S3Client:
    """
    Client for AWS S3.
    """

    def __init__(self, bucket: str) -> None:
        self.client = boto3.client("s3")
        self.bucket = bucket

    def upload(self, key: str, payload: bytes) -> None:
        """
        Upload `payload` as `package_name`.
        """
        self.client.upload_fileobj(Fileobj=payload, Bucket=self.bucket, Key=key)

    def get_sha256(self, key: str):
        fileobj = BytesIO()
        self.client.download_fileobj(Bucket=self.bucket, Key=key, Fileobj=fileobj)
        fileobj.seek(0)
        return hashlib.sha256(fileobj.read()).hexdigest()

    def get_presigned_download_url(self, key: str, expires_in: int) -> str:
        """
        Get presigned URL for `package_name`.
        """
        response = self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": key},
            ExpiresIn=expires_in,
        )
        return response

    def get_object(self, key: str) -> BytesIO:
        """
        Get presigned URL for `package_name`.
        """
        return self.client.get_object(Bucket=self.bucket, Key=key)
