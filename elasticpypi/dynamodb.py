import urllib

import boto3
from boto3.dynamodb.conditions import Key

from elasticpypi.config import config
from elasticpypi.s3 import S3Client
from elasticpypi.name import compute_package_name, normalize, compute_version


class DynamoDBClient:
    def __init__(self):
        self.s3_client = S3Client()
        self.resource = boto3.resource("dynamodb")
        self.table = self.resource.Table(config["table"])

    def list_packages(self):
        dynamodb_packages = self.table.scan(ProjectionExpression="normalized_name")
        package_set = set()
        for package in dynamodb_packages["Items"]:
            package_set.add(package["normalized_name"])
        packages = [(package, package) for package in sorted(package_set)]
        return packages

    def list_packages_by_name(self, package_name):
        normalized_name = normalize(package_name)
        dynamodb_packages = self.table.query(
            IndexName="normalized_name-index",
            KeyConditionExpression=Key("normalized_name").eq(normalized_name),
            ProjectionExpression="filename",
            ScanIndexForward=False,
        )
        sorted_packages = sorted(
            dynamodb_packages["Items"], key=lambda k: k["filename"]
        )
        packages = []
        for package in sorted_packages:
            filename = package["filename"]
            packages.append(
                {
                    "filename": filename,
                    "download_url": self.s3_client.get_presigned_download_url(filename),
                }
            )
        return packages

    def delete_item(self, filename):
        version = compute_version(filename)
        self.table.delete_item(Key={"package_name": filename, "version": version})

    def put_item(self, filename):
        version = compute_version(filename)
        normalized_name = normalize(filename)
        data = {
            "package_name": filename,
            "version": version,
            "filename": filename,
            "normalized_name": normalized_name,
        }
        self.table.put_item(Item=data)
        return data

    def exists(self, filename):
        dynamodb_packages = self.table.query(
            KeyConditionExpression=Key("package_name").eq(filename),
            ProjectionExpression="filename",
            ScanIndexForward=False,
        )
        return dynamodb_packages.get("Count", 0)
