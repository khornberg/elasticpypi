from boto3.dynamodb.conditions import Key
from elasticpypi import name
from elasticpypi import s3
from elasticpypi.config import config

TABLE = config['table']


def list_packages(dynamodb):
    table = dynamodb.Table(TABLE)
    dynamodb_packages = table.scan(ProjectionExpression='package_name')
    package_set = set()
    for package in dynamodb_packages['Items']:
        package_set.add(package['package_name'])
    packages = [(package, package) for package in sorted(package_set)]
    return packages


def list_packages_by_name(dynamodb, package_name):
    _name = name.normalize(package_name)
    table = dynamodb.Table(TABLE)
    dynamodb_packages = table.query(
        IndexName='normalized_name-index',
        KeyConditionExpression=Key('normalized_name').eq(_name),
        ProjectionExpression='filename',
        ScanIndexForward=False,
    )
    packages = [(s3.signed_url(package['filename']), package['filename']) for package in dynamodb_packages['Items']]
    return packages
