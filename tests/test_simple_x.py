from flask_testing import TestCase
from base64 import b64encode
from elasticpypi.api import app
from elasticpypi.config import config
from tests import fixtures
from moto import mock_dynamodb2
from tests import mock_dynamodb_table

TABLE = config['table']


class ElasticPypiTests(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        password = config['password']
        username = config['username']
        basic_hash = '{0}:{1}'.format(username, password)
        self.headers = {'Authorization': 'Basic ' + b64encode(basic_hash.encode('utf-8')).decode()}

    def test_get_simple_x_401(self):
        response = self.client.get('/simple/x/')
        self.assert401(response)

    @mock_dynamodb2
    def test_get_simple_x_200_from_dynamodb(self):
        mock_dynamodb_table.make_table([
            {
                'package_name': 'z-0.tar.gz',
                'version': '0',
                'normalized_name': 'z',
                'filename': 'z-0.tar.gz'
            }, {
                'package_name': 'y-0.tar.gz',
                'version': '0',
                'normalized_name': 'y',
                'filename': 'y-0.tar.gz'
            }, {
                'package_name': 'x-0.tar.gz',
                'version': '0',
                'normalized_name': 'x',
                'filename': 'x-0.tar.gz'
            }, {
                'package_name': 'x-1.tar.gz',
                'version': '1',
                'normalized_name': 'x',
                'filename': 'x-1.tar.gz'
            }
        ])
        response = self.client.get('/simple/x/', headers=self.headers)
        self.assert200(response)
        self.assertEqual(response.data.decode(), fixtures.links_html)
