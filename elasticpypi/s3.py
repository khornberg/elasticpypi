import boto3

from elasticpypi.config import config


class S3Client:
    def __init__(self):
        self.client = boto3.client("s3")
        self.bucket = config["bucket"]

    def upload(self, filename, payload):
        self.client.upload_fileobj(payload, self.bucket, filename)

    def get_presigned_download_url(self, filename):
        response = self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": filename},
            ExpiresIn=3600,
        )
        return response
