from typing import Dict, List, Optional

import boto3
from boto3.dynamodb.conditions import Key

from elasticpypi.name import normalize_name, normalize_version
from elasticpypi.package import Package


class DynamoDBClient:
    """
    AWS DynamoDB client.
    """

    def __init__(self, table_name: str) -> None:
        self.resource = boto3.resource("dynamodb")
        self.table = self.resource.Table(table_name)

    def list_normalized_names(self) -> List[str]:
        """
        List all package normalized names.
        """
        dynamodb_packages = self.table.scan(ProjectionExpression="normalized_name")
        normalized_name_set = set()
        for item in dynamodb_packages["Items"]:
            normalized_name_set.add(item["normalized_name"])
        return list(normalized_name_set)

    def list_packages_by_name(self, normalized_name: str) -> List[Package]:
        """
        List package names by `normalized_name`.
        """
        dynamodb_packages = self.table.query(
            IndexName="normalized_name-index",
            KeyConditionExpression=Key("normalized_name").eq(normalized_name),
            ProjectionExpression="package_name,normalized_name,version,sha256",
            ScanIndexForward=False,
        )
        packages: List[Package] = []
        for package_data in dynamodb_packages["Items"]:
            package = Package(
                name=package_data["package_name"],
                normalized_name=package_data["normalized_name"],
                version=package_data["version"],
                sha256=package_data.get("sha256", ""),
            )
            packages.append(package)
        packages.sort(key=lambda k: k.name)
        return packages

    def delete_item(self, package_name: str, version: Optional[str] = None) -> None:
        """
        Delete item with `package_name`.
        """
        if not version:
            version = normalize_version(package_name)

        self.table.delete_item(Key={"package_name": package_name, "version": version})

    def put_item(self, package_name: str, package_sha256: str) -> Dict[str, str]:
        """
        Add item with `package_name`.
        """
        version = normalize_version(package_name)
        normalized_name = normalize_name(package_name)
        data = {
            "package_name": package_name,
            "version": version,
            "normalized_name": normalized_name,
            "sha256": package_sha256,
        }
        self.table.put_item(Item=data)
        return data

    def exists(self, package_name: str) -> bool:
        """
        Check if `package_name` exists in DB.
        """
        dynamodb_packages = self.table.query(
            KeyConditionExpression=Key("package_name").eq(package_name),
            ProjectionExpression="package_name",
            ScanIndexForward=False,
        )
        return dynamodb_packages.get("Count", 0)
