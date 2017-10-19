from flask_testing import TestCase
from base64 import b64encode
import mock
import io
from elasticpypi.api import app
from elasticpypi.config import config


class ElasticPypiTests(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        password = config['password']
        username = config['username']
        basic_hash = '{0}:{1}'.format(username, password)
        self.headers = {'Authorization': 'Basic ' + b64encode(basic_hash.encode('utf-8')).decode()}

    def test_get_packages_x_401(self):
        response = self.client.get('/packages/x')
        self.assert401(response)

    @mock.patch('elasticpypi.s3.download')
    def test_get_packages_x_200(self, download):
        f = io.BytesIO('hello'.encode('utf-8'))
        download.return_value = f
        response = self.client.get('/packages/x', headers=self.headers)
        self.assert200(response)
        self.assertEquals(response.data, b'hello')
        f.close()
