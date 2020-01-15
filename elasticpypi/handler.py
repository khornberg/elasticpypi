from basicauth import decode

from elasticpypi.config import config
from elasticpypi.auth import AuthPolicy
from elasticpypi.dynamodb import DynamoDBClient


def s3(event, _context):
    filename = event.get("Records")[0]["s3"]["object"]["key"]
    dynamodb_client = DynamoDBClient()
    if "Delete" in event["Records"][0]["eventName"]:
        dynamodb_client.delete_item(filename)
        return None
    dynamodb_client.put_item(filename)
    return None


def auth(event, _context):
    user, pwd = decode(event["headers"]["Authorization"])
    if user != config["username"] or pwd != config["password"]:
        raise Exception("Unauthorized")
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
