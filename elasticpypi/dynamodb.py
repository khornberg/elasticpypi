import urllib

import boto3
from boto3.dynamodb.conditions import Key

from elasticpypi.config import config
from elasticpypi.s3 import S3Client
from elasticpypi.name import normalize, compute_version


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

    def list_packages_by_name(self, normalized_name):
        dynamodb_packages = self.table.query(
            IndexName="normalized_name-index",
            KeyConditionExpression=Key("normalized_name").eq(normalized_name),
            ProjectionExpression="package_name",
            ScanIndexForward=False,
        )
        packages = dynamodb_packages["Items"]
        packages.sort(key=lambda k: k["package_name"])
        for package in packages:
            package_name = package["package_name"]
            package["download_url"] = self.s3_client.get_presigned_download_url(
                package_name
            )
        return packages

    def delete_item(self, package_name):
        version = compute_version(package_name)
        self.table.delete_item(Key={"package_name": package_name, "version": version})

    def put_item(self, package_name):
        version = compute_version(package_name)
        normalized_name = normalize(package_name)
        data = {
            "package_name": package_name,
            "version": version,
            "normalized_name": normalized_name,
        }
        self.table.put_item(Item=data)
        return data

    def exists(self, package_name):
        dynamodb_packages = self.table.query(
            KeyConditionExpression=Key("package_name").eq(package_name),
            ProjectionExpression="package_name",
            ScanIndexForward=False,
        )
        return dynamodb_packages.get("Count", 0)
