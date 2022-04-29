import boto3
from basicauth import decode
from elasticpypi.name import compute_package_name, normalize, compute_version
from elasticpypi.config import config
from elasticpypi.auth import AuthPolicy
from elasticpypi import dynamodb

TABLE = config["table"]


def s3(event, context):
    dynamodb_resource = boto3.resource("dynamodb")
    table = dynamodb_resource.Table(TABLE)
    filename = event.get("Records")[0]["s3"]["object"]["key"]
    package_name = compute_package_name(filename)
    version = compute_version(filename)
    normalized_name = normalize(package_name)
    if "Delete" in event["Records"][0]["eventName"]:
        dynamodb.delete_item(version, table, filename)
        return None
    dynamodb.put_item(version, filename, normalized_name, table)
    return None


def auth(event, context):
    authorization_header = {k.lower(): v for k, v in event["headers"].items() if k.lower() == "authorization"}
    # Get the username:password hash from the authorization header
    username_password_hash = authorization_header["authorization"].split()[1]
    user, pwd = decode(username_password_hash)
    if config.get("username") and config.get("password"):
        users = {config.get("username"): config.get("password")}
    if config.get("users"):
        pairs = config.get("users").split(",")
        users = {}
        for pair in pairs:
            username, password = pair.split(":")
            users[username] = password
    if not users.get(user) or users.get(user) != pwd:
        raise Exception("Unauthorized")
    principal_id = user
    tmp = event["methodArn"].split(":")
    api_gateway_arn_tmp = tmp[5].split("/")
    aws_account_id = tmp[4]
    policy = AuthPolicy(principal_id, aws_account_id)
    policy.restApiId = api_gateway_arn_tmp[0]
    policy.region = tmp[3]
    policy.stage = api_gateway_arn_tmp[1]
    policy.allow_all_methods()
    return policy.build()
