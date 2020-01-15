"""
Client for AWS S3.
"""
import boto3

from elasticpypi.config import config


class S3Client:
    """
    Client for AWS S3.
    """

    def __init__(self):
        self.client = boto3.client("s3")
        self.bucket = config["bucket"]

    def upload(self, package_name: str, payload: bytes) -> None:
        """
        Upload `payload` as `package_name`.
        """
        self.client.upload_fileobj(payload, self.bucket, package_name)

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
