import boto3
from elasticpypi.config import config

TABLE = config['table']


def add_items(table, items=None):
    default_items = [
        {
            'package_name': 'z',
            'version': '0',
            'normalized_name': 'z',
            'filename': 'z-0.tar.gz'
        }, {
            'package_name': 'y',
            'version': '0',
            'normalized_name': 'y',
            'filename': 'y-0.tar.gz'
        }, {
            'package_name': 'x',
            'version': '0',
            'normalized_name': 'x',
            'filename': 'x-0.tar.gz'
        }, {
            'package_name': 'x-y-z',
            'version': '0',
            'normalized_name': 'x-y-z',
            'filename': 'x-y-z-0.tar.gz'
        }, {
            'package_name': 'x.y.z',
            'version': '1',
            'normalized_name': 'x-y-z',
            'filename': 'x.y.z-1.tar.gz'
        }, {
            'package_name': 'xy',
            'version': '1',
            'normalized_name': 'xy',
            'filename': 'Xy-1.tar.gz'
        }
    ]
    _items = items if items else default_items
    for item in _items:
        table.put_item(Item=item)


def make_table(items=None):
    dynamodb = boto3.resource('dynamodb', region_name='artic-1')
    table = dynamodb.create_table(
        TableName=TABLE,
        KeySchema=[
            {
                'AttributeName': 'package_name',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'version',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'package_name',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'version',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'filename',
                'AttributeType': 'S'
            },
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'normalized_name-index',
                'KeySchema': [{
                    'AttributeName': 'normalized_name',
                    'KeyType': 'HASH'
                }, ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            },
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 1,
                               'WriteCapacityUnits': 1}
    )
    add_items(table, items)
    return table
