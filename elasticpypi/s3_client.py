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

    def upload(self, package_name: str, payload: bytes) -> None:
        """
        Upload `payload` as `package_name`.
        """
        self.client.upload_fileobj(
            Fileobj=payload, Bucket=self.bucket, Key=package_name
        )

    def get_sha256(self, package_name: str):
        fileobj = BytesIO()
        self.client.download_fileobj(
            Bucket=self.bucket, Key=package_name, Fileobj=fileobj
        )
        fileobj.seek(0)
        return hashlib.sha256(fileobj.read()).hexdigest()

    def get_presigned_download_url(self, package_name: str) -> str:
        """
        Get presigned URL for `package_name`.
        """
        response = self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": package_name},
            ExpiresIn=3600,
        )
        return response
