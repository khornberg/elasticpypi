import os

from basicauth import decode

from elasticpypi.auth import AuthPolicy
from elasticpypi.dynamodb_client import DynamoDBClient
from elasticpypi.env_namespace import EnvNamespace
from elasticpypi.s3_client import S3Client


def s3(event, _context):
    env_namespace = EnvNamespace(os.environ)
    print(f"S3 event: {event}")
    s3_object = event.get("Records")[0]["s3"]["object"]
    print(f"Got S3 object: {s3_object}")
    package_name = s3_object["key"]
    dynamodb_client = DynamoDBClient(env_namespace.table)
    if "Delete" in event["Records"][0]["eventName"]:
        print(f"Deleting file from dynamo: {package_name}")
        dynamodb_client.delete_item(package_name)
        return None

    print(f"Adding file to dynamo: {package_name}")
    s3_client = S3Client()
    package_sha256 = s3_client.get_sha256(package_name)
    dynamodb_client.put_item(package_name, package_sha256)
    return None


def auth(event, _context):
    env_namespace = EnvNamespace(os.environ)
    user, pwd = decode(event["headers"]["Authorization"])
    if user != env_namespace.username or pwd != env_namespace.password:
        raise ValueError("Unauthorized")

    principalId = user
    tmp = event["methodArn"].split(":")
    apiGatewayArnTmp = tmp[5].split("/")
    awsAccountId = tmp[4]
    policy = AuthPolicy(principalId, awsAccountId)
    policy.restApiId = apiGatewayArnTmp[0]
    policy.region = tmp[3]
    policy.stage = apiGatewayArnTmp[1]
    policy.allowAllMethods()
    authResponse = policy.build()
    return authResponse
