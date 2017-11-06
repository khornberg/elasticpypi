import boto3
import urllib
from elasticpypi.name import compute_package_name, normalize, compute_version
from elasticpypi.config import config

TABLE = config['table']


def s3(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(TABLE)
    filename = event.get('Records')[0]['s3']['object']['key']
    package_name = compute_package_name(filename)
    version = compute_version(filename)
    normalized_name = normalize(package_name)
    if 'Delete' in event['Records'][0]['eventName']:
        delete_item(version, table, filename)
        return None
    put_item(version, filename, normalized_name, table)
    return None


def delete_item(version, table, filename):
    table.delete_item(
        Key={
            'package_name': filename,
            'version': version,
        },
    )


def put_item(version, filename, normalized_name, table):
    table.put_item(
        Item={
            'package_name': urllib.unquote_plus(filename),
            'version': urllib.unquote_plus(version),
            'filename': urllib.unquote_plus(filename),
            'normalized_name': urllib.unquote_plus(normalized_name),
        }
    )
