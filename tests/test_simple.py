import io
from unittest import mock
from flask_testing import TestCase
from elasticpypi.api import app
from elasticpypi.config import config
from tests import fixtures
from moto import mock_dynamodb
from tests import mock_dynamodb_table

TABLE = config["table"]


class SimpleTests(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        return app

    @mock_dynamodb
    def test_get_simple_200_from_dynamodb(self):
        mock_dynamodb_table.make_table(
            items=[
                {"package_name": "z.zip", "normalized_name": "z", "version": "0"},
                {"package_name": "y-0.zip", "normalized_name": "y", "version": "0"},
                {"package_name": "y-1.zip", "normalized_name": "y", "version": "1"},
                {"package_name": "x.zip", "normalized_name": "x", "version": "0"},
            ]
        )
        response = self.client.get("/simple/")
        self.assert200(response)
        self.assertEqual(response.data.decode(), fixtures.simple_html)

    @mock_dynamodb
    @mock.patch("elasticpypi.s3.upload")
    def test_post_simple_200(self, upload):
        mock_dynamodb_table.make_table(
            items=[
                {
                    "package_name": "py-0.0.1.tar.gz",
                    "normalized_name": "py",
                    "version": "0.1.2",
                    "filename": "py-0.0.1.tar.gz",
                }
            ]
        )
        f = io.BytesIO("hello".encode("utf-8"))
        response = self.client.post("/simple/", data={"content": (f, "py-0.1.2.tar.gz")})
        self.assertStatus(response, 200)
        upload.assert_called_with("py-0.1.2.tar.gz", mock.ANY)
        f.close()

    @mock.patch("elasticpypi.s3.upload")
    def test_cannot_post_file_with_slash_in_the_file_name(self, upload):
        f = io.BytesIO("hello".encode("utf-8"))
        response = self.client.post("/simple/", data={"content": (f, "../py-0.1.2.tar.gz")})
        self.assert400(response)
        assert not upload.called
        f.close()

    @mock_dynamodb
    @mock.patch("elasticpypi.s3.upload")
    def test_cannot_post_file_when_package_already_exists_and_overwrite_is_false(self, upload):
        mock_dynamodb_table.make_table(
            items=[
                {
                    "package_name": "py-0.1.2.tar.gz",
                    "normalized_name": "py",
                    "version": "0.1.2",
                    "filename": "py-0.1.2.tar.gz",
                }
            ]
        )
        f = io.BytesIO("hello".encode("utf-8"))
        response = self.client.post("/simple/", data={"content": (f, "py-0.1.2.tar.gz")})
        self.assertEqual(response.status_code, 409)
        assert not upload.called
        f.close()

    @mock_dynamodb
    @mock.patch("elasticpypi.s3.upload")
    @mock.patch("elasticpypi.api.config")
    def test_can_post_file_when_package_exists_and_overwrite_is_true(self, config, upload):
        mock_dynamodb_table.make_table(
            items=[
                {
                    "package_name": "py-0.1.2.tar.gz",
                    "normalized_name": "py",
                    "version": "0.1.2",
                    "filename": "py-0.1.2.tar.gz",
                }
            ]
        )
        config.return_value = {"OVERWRITE": "true"}
        f = io.BytesIO("hello".encode("utf-8"))
        response = self.client.post("/simple/", data={"content": (f, "py-0.1.2.tar.gz")})
        self.assertStatus(response, 200)
        upload.assert_called_with("py-0.1.2.tar.gz", mock.ANY)
        f.close()
