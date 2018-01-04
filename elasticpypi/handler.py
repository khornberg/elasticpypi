import boto3
from basicauth import decode
from elasticpypi.name import compute_package_name, normalize, compute_version
from elasticpypi.config import config
from elasticpypi.auth import AuthPolicy
from elasticpypi import dynamodb

TABLE = config['table']


def s3(event, context):
    dynamodbResource = boto3.resource('dynamodb')
    table = dynamodbResource.Table(TABLE)
    filename = event.get('Records')[0]['s3']['object']['key']
    package_name = compute_package_name(filename)
    version = compute_version(filename)
    normalized_name = normalize(package_name)
    if 'Delete' in event['Records'][0]['eventName']:
        dynamodb.delete_item(version, table, filename)
        return None
    dynamodb.put_item(version, filename, normalized_name, table)
    return None


def auth(event, context):
    user, pwd = decode(event['headers']['Authorization'])
    if user != config['username'] or pwd != config['password']:
        raise Exception('Unauthorized')
    principalId = user
    tmp = event['methodArn'].split(':')
    apiGatewayArnTmp = tmp[5].split('/')
    awsAccountId = tmp[4]
    policy = AuthPolicy(principalId, awsAccountId)
    policy.restApiId = apiGatewayArnTmp[0]
    policy.region = tmp[3]
    policy.stage = apiGatewayArnTmp[1]
    policy.allowAllMethods()
    authResponse = policy.build()
    return authResponse
