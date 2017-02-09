from unittest import TestCase
from elasticpypi.config import config
from elasticpypi.dynamodb import list_packages_by_name
import boto3
from moto import mock_dynamodb2

TABLE = config['table']


@mock_dynamodb2
class ElasticPypiDynamodbTests(TestCase):

    def setUp(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='artic-1')
        self.table = self.make_table()
        self.add_items(self.table)

    def tearDown(self):
        self.table.delete()

    def test_list_packages_by_name_pip8_single_word(self):
        packages = list_packages_by_name(self.dynamodb, 'x')
        signed_url, package_name = packages[0]
        self.assertEqual(1, len(packages))
        self.assertIn('s3.amazonaws.com/x-0.tar.gz', signed_url)
        self.assertEqual('x-0.tar.gz', package_name)

    def test_list_packages_by_name_pip7_single_word(self):
        packages = list_packages_by_name(self.dynamodb, 'Xy')
        signed_url, package_name = packages[0]
        self.assertEqual(1, len(packages))
        self.assertIn('s3.amazonaws.com/Xy-1.tar.gz', signed_url)
        self.assertEqual('Xy-1.tar.gz', package_name)

    def test_list_packages_by_name_pip8_single_word_not_found(self):
        packages = list_packages_by_name(self.dynamodb, 'a')
        self.assertEqual([], packages)

    def test_list_packages_by_name_pip8_name_spaced_package(self):
        packages = list_packages_by_name(self.dynamodb, 'x-y-z')
        signed_url, package_name = packages[0]
        signed_url1, package_name1 = packages[1]
        self.assertEqual(2, len(packages))
        self.assertIn('s3.amazonaws.com/x-y-z-0.tar.gz', signed_url)
        self.assertEqual('x-y-z-0.tar.gz', package_name)
        self.assertIn('s3.amazonaws.com/x.y.z-1.tar.gz', signed_url1)
        self.assertEqual('x.y.z-1.tar.gz', package_name1)

    def test_list_packages_by_name_pip7_name_spaced_package(self):
        packages = list_packages_by_name(self.dynamodb, 'x.y.z')
        signed_url, package_name = packages[0]
        signed_url1, package_name1 = packages[1]
        self.assertEqual(2, len(packages))
        self.assertIn('s3.amazonaws.com/x-y-z-0.tar.gz', signed_url)
        self.assertEqual('x-y-z-0.tar.gz', package_name)
        self.assertIn('s3.amazonaws.com/x.y.z-1.tar.gz', signed_url1)
        self.assertEqual('x.y.z-1.tar.gz', package_name1)

    def make_table(self):
        # dynamodb = boto3.resource('dynamodb')
        table = self.dynamodb.create_table(
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
                'filename': 'z-0.tar.gz'
            }, {
                'package_name': 'y',
                'version': '0',
                'filename': 'y-0.tar.gz'
            }, {
                'package_name': 'x',
                'version': '0',
                'filename': 'x-0.tar.gz'
            }, {
                'package_name': 'x-y-z',
                'version': '0',
                'filename': 'x-y-z-0.tar.gz'
            }, {
                'package_name': 'x-y-z',
                'version': '1',
                'filename': 'x.y.z-1.tar.gz'
            }, {
                'package_name': 'xy',
                'version': '1',
                'filename': 'Xy-1.tar.gz'
            }
        ]
        _items = items if items else default_items
        for item in _items:
            table.put_item(Item=item)
