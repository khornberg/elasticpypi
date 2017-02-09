from flask_testing import TestCase
from base64 import b64encode
import mock
import io
from elasticpypi.api import app
from elasticpypi.config import config
from tests import fixtures
import boto3
from moto import mock_dynamodb2

TABLE = config['table']


class SimpleTests(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        password = config['password']
        username = config['username']
        self.headers = {'Authorization': 'Basic ' + b64encode("{0}:{1}".format(username, password))}

    def test_get_simple_401(self):
        response = self.client.get('/simple/')
        self.assert401(response)

    def test_post_simple_401(self):
        response = self.client.post('/simple/')
        self.assert401(response)

    @mock_dynamodb2
    def test_get_simple_200_from_dynamodb(self):
        table = self.make_table()
        self.add_items(table)
        response = self.client.get('/simple/', headers=self.headers)
        self.assert200(response)
        self.assertEqual(response.data, fixtures.simple_html)

    @mock.patch('elasticpypi.s3.exists')
    @mock.patch('elasticpypi.s3.upload')
    def test_post_simple_200(self, upload, exists):
        exists.return_value = False
        f = io.BytesIO('hello'.encode('utf-8'))
        response = self.client.post('/simple/', headers=self.headers, data={'content': (f, 'py-0.1.2.tar.gz')})
        self.assert200(response)
        upload.assert_called_with('py-0.1.2.tar.gz', mock.ANY)
        f.close()

    @mock.patch('elasticpypi.s3.upload')
    def test_cannot_post_file_with_slash_in_the_file_name(self, upload):
        f = io.BytesIO('hello'.encode('utf-8'))
        response = self.client.post('/simple/', headers=self.headers, data={'content': (f, '../py-0.1.2.tar.gz')})
        self.assert400(response)
        assert not upload.called
        f.close()

    @mock.patch('elasticpypi.s3.list_packages')
    @mock.patch('elasticpypi.s3.upload')
    def test_cannot_post_file_when_package_already_exists_and_overwrite_is_false(self, upload, list_packages):
        list_packages.return_value = ['py-0.1.2.tar.gz']
        f = io.BytesIO('hello'.encode('utf-8'))
        response = self.client.post('/simple/', headers=self.headers, data={'content': (f, 'py-0.1.2.tar.gz')})
        self.assertEqual(response.status_code, 409)
        list_packages.assert_called_with('py-0.1.2.tar.gz', True)
        assert not upload.called
        f.close()

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
                'version': '0'
            }, {
                'package_name': 'y',
                'version': '0'
            }, {
                'package_name': 'x',
                'version': '0'
            }
        ]
        _items = items if items else default_items
        for item in _items:
            table.put_item(Item=item)
