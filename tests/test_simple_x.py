import re
import boto3
from flask_testing import TestCase
from base64 import b64encode
from elasticpypi.api import app
from elasticpypi.config import config
from tests import fixtures
from moto import mock_dynamodb2

TABLE = config['table']


class ElasticPypiTests(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        password = config['password']
        username = config['username']
        self.headers = {'Authorization': 'Basic ' + b64encode("{0}:{1}".format(username, password))}

    def test_get_simple_x_401(self):
        response = self.client.get('/simple/x/')
        self.assert401(response)

    @mock_dynamodb2
    def test_get_simple_x_200_from_dynamodb(self):
        table = self.make_table()
        self.add_items(table)
        response = self.client.get('/simple/x/', headers=self.headers)
        html = re.sub("href=\"https://.*\"", "href=\"https://\"", response.data)  # Remove signed url since it changes
        self.assert200(response)
        self.assertEqual(html, fixtures.links_html)

    def make_table(self):
        dynamodb = boto3.resource('dynamodb')
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
            ],
            ProvisionedThroughput={'ReadCapacityUnits': 1,
                                   'WriteCapacityUnits': 1}
        )
        return table

    def add_items(self, table, items=None):
        default_items = [
            {
                'package_name': 'z',
                'version': '0',
                'filename': 'x-0.tar.gz'
            }, {
                'package_name': 'y',
                'version': '0',
                'filename': 'x-0.tar.gz'
            }, {
                'package_name': 'x',
                'version': '0',
                'filename': 'x-0.tar.gz'
            }, {
                'package_name': 'x',
                'version': '1',
                'filename': 'x-1.tar.gz'
            }
        ]
        _items = items if items else default_items
        for item in _items:
            table.put_item(Item=item)
