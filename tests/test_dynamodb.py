from unittest import TestCase
from elasticpypi.dynamodb import list_packages_by_name
from elasticpypi.handler import s3
from tests.fixtures import delete_event, put_event
from moto import mock_dynamodb2
from tests import mock_dynamodb_table
import boto3


@mock_dynamodb2
class ElasticPypiDynamodbTests(TestCase):

    def setUp(self):
        self.dynamodb = boto3.resource('dynamodb', region_name='artic-1')
        self.table = mock_dynamodb_table.make_table()

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
        self.assertIn('s3.amazonaws.com/x.y.z-1.tar.gz', signed_url)
        self.assertEqual('x.y.z-1.tar.gz', package_name)
        self.assertIn('s3.amazonaws.com/x-y-z-0.tar.gz', signed_url1)
        self.assertEqual('x-y-z-0.tar.gz', package_name1)

    def test_list_packages_by_name_pip7_name_spaced_package(self):
        packages = list_packages_by_name(self.dynamodb, 'x.y.z')
        signed_url, package_name = packages[0]
        signed_url1, package_name1 = packages[1]
        self.assertEqual(2, len(packages))
        self.assertIn('s3.amazonaws.com/x.y.z-1.tar.gz', signed_url)
        self.assertEqual('x.y.z-1.tar.gz', package_name)
        self.assertIn('s3.amazonaws.com/x-y-z-0.tar.gz', signed_url1)
        self.assertEqual('x-y-z-0.tar.gz', package_name1)

    def test_record_deleted_when_delete_events_occur(self):
        s3(delete_event, None)
        self.assertFalse(self.table.get_item(Key={'package_name': 'z', 'version': '0'}).get('Item'))

    def test_record_created_when_put_events_occur(self):
        self.assertFalse(self.table.get_item(Key={'package_name': 'a', 'version': '0'}).get('Item'))
        s3(put_event, None)
        item = self.table.get_item(Key={'package_name': 'a', 'version': '0'}).get('Item')
        self.assertEqual({'normalized_name': 'a', 'version': '0', 'package_name': 'a', 'filename': 'a-0.tar.gz'}, item)
