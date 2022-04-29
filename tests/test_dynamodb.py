from unittest import TestCase
from elasticpypi.dynamodb import list_packages_by_name
from elasticpypi.handler import s3
from tests.fixtures import delete_event, put_event, put_event_for_wheel
from moto import mock_dynamodb
from tests import mock_dynamodb_table
import boto3


@mock_dynamodb
class ElasticPypiDynamodbTests(TestCase):
    def setUp(self):
        self.dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
        self.table = mock_dynamodb_table.make_table()

    def tearDown(self):
        self.table.delete()

    def test_list_packages_by_name_pip8_single_word(self):
        packages = list_packages_by_name(self.dynamodb, "x")
        url, package_name = packages[0]
        self.assertEqual(1, len(packages))
        self.assertIn("x-0.tar.gz", url)
        self.assertEqual("x-0.tar.gz", package_name)

    def test_list_packages_by_name_pip7_single_word(self):
        packages = list_packages_by_name(self.dynamodb, "Xy")
        url, package_name = packages[0]
        self.assertEqual(1, len(packages))
        self.assertIn("Xy-1.tar.gz", url)
        self.assertEqual("Xy-1.tar.gz", package_name)

    def test_list_packages_by_name_pip8_single_word_not_found(self):
        packages = list_packages_by_name(self.dynamodb, "a")
        self.assertEqual([], packages)

    def test_list_packages_by_name_pip8_name_spaced_package(self):
        packages = list_packages_by_name(self.dynamodb, "x-y-z")
        url, package_name = packages[0]
        url1, package_name1 = packages[1]
        self.assertEqual(2, len(packages))
        self.assertIn("x-y-z-0.tar.gz", url)
        self.assertEqual("x-y-z-0.tar.gz", package_name)
        self.assertIn("x.y.z-1.tar.gz", url1)
        self.assertEqual("x.y.z-1.tar.gz", package_name1)

    def test_list_packages_by_name_pip7_name_spaced_package(self):
        packages = list_packages_by_name(self.dynamodb, "x.y.z")
        url, package_name = packages[0]
        url1, package_name1 = packages[1]
        self.assertEqual(2, len(packages))
        self.assertIn("x-y-z-0.tar.gz", url)
        self.assertEqual("x-y-z-0.tar.gz", package_name)
        self.assertIn("x.y.z-1.tar.gz", url1)
        self.assertEqual("x.y.z-1.tar.gz", package_name1)

    def test_record_deleted_when_delete_events_occur(self):
        s3(delete_event, None)
        self.assertFalse(self.table.get_item(Key={"package_name": "z", "version": "0"}).get("Item"))

    def test_record_created_with_url_quoted_file_names(self):
        self.assertFalse(self.table.get_item(Key={"package_name": "a b-0.tar.gz", "version": "0"}).get("Item"))
        s3(put_event(), None)
        item = self.table.get_item(Key={"package_name": "a b-0.tar.gz", "version": "0"}).get("Item")
        self.assertEqual(
            {"normalized_name": "a b", "version": "0", "package_name": "a b-0.tar.gz", "filename": "a b-0.tar.gz"}, item
        )

    def test_record_created_for_various_package_suffices(self):
        self.assertFalse(self.table.get_item(Key={"package_name": "a-0.zip", "version": "0"}).get("Item"))
        s3(put_event(package_name="a-0.zip"), None)
        item = self.table.get_item(Key={"package_name": "a-0.zip", "version": "0"}).get("Item")
        self.assertEqual(
            {"normalized_name": "a", "version": "0", "package_name": "a-0.zip", "filename": "a-0.zip"}, item
        )
        self.assertFalse(self.table.get_item(Key={"package_name": "a-0.tar.bz3", "version": "0"}).get("Item"))
        s3(put_event(package_name="a-0.tar.bz3"), None)
        item = self.table.get_item(Key={"package_name": "a-0.tar.bz3", "version": "0"}).get("Item")
        self.assertEqual(
            {"normalized_name": "a", "version": "0", "package_name": "a-0.tar.bz3", "filename": "a-0.tar.bz3"}, item
        )

    def test_record_created_when_put_wheel_events_occur(self):
        self.assertFalse(
            self.table.get_item(Key={"package_name": "z-0-cp34-cp34m-manylinux1_x86_64.whl", "version": "0"}).get(
                "Item"
            )
        )
        s3(put_event_for_wheel, None)
        item = self.table.get_item(Key={"package_name": "z-0-cp34-cp34m-manylinux1_x86_64.whl", "version": "0"}).get(
            "Item"
        )
        self.assertEqual(
            {
                "normalized_name": "z",
                "version": "0",
                "package_name": "z-0-cp34-cp34m-manylinux1_x86_64.whl",
                "filename": "z-0-cp34-cp34m-manylinux1_x86_64.whl",
            },
            item,
        )
