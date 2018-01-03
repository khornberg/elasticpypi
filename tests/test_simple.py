import io
from unittest import mock
from flask_testing import TestCase
from base64 import b64encode
from elasticpypi.api import app
from elasticpypi.config import config
from tests import fixtures
from moto import mock_dynamodb2
from tests import mock_dynamodb_table

TABLE = config['table']


class SimpleTests(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        password = config['password']
        username = config['username']
        basic_hash = '{0}:{1}'.format(username, password)
        self.headers = {'Authorization': 'Basic ' + b64encode(basic_hash.encode('utf-8')).decode()}

    @mock_dynamodb2
    def test_get_simple_200_from_dynamodb(self):
        mock_dynamodb_table.make_table(items=[
            {
                'package_name': 'z.zip',
                'normalized_name': 'z',
                'version': '0'
            }, {
                'package_name': 'y-0.zip',
                'normalized_name': 'y',
                'version': '0'
            }, {
                'package_name': 'y-1.zip',
                'normalized_name': 'y',
                'version': '1'
            }, {
                'package_name': 'x.zip',
                'normalized_name': 'x',
                'version': '0'
            }
        ])
        response = self.client.get('/simple/', headers=self.headers)
        self.assert200(response)
        self.assertEqual(response.data.decode(), fixtures.simple_html)

    @mock.patch('elasticpypi.s3.exists')
    @mock.patch('elasticpypi.s3.upload')
    def test_post_simple_200(self, upload, exists):
        exists.return_value = False
        f = io.BytesIO('hello'.encode('utf-8'))
        response = self.client.post('/simple/', headers=self.headers, data={'content': (f, 'py-0.1.2.tar.gz')})
        self.assertStatus(response, 200)
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

    @mock.patch('elasticpypi.s3.exists')
    @mock.patch('elasticpypi.s3.upload')
    @mock.patch('elasticpypi.api.config')
    def test_can_post_file_when_package_exists_and_overwrite_is_true(self, config, upload, exists):
        config.return_value = {'OVERWRITE': 'true'}
        exists.return_value = True
        f = io.BytesIO('hello'.encode('utf-8'))
        response = self.client.post('/simple/', headers=self.headers, data={'content': (f, 'py-0.1.2.tar.gz')})
        self.assertStatus(response, 200)
        upload.assert_called_with('py-0.1.2.tar.gz', mock.ANY)
        f.close()
