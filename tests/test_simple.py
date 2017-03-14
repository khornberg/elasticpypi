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
        self.headers = {'Authorization': 'Basic ' + b64encode("{0}:{1}".format(username, password))}

    def test_get_simple_401(self):
        response = self.client.get('/simple/')
        self.assert401(response)

    @mock_dynamodb2
    def test_get_simple_200_from_dynamodb(self):
        mock_dynamodb_table.make_table(items=[
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
        ])
        response = self.client.get('/simple/', headers=self.headers)
        self.assert200(response)
        self.assertEqual(response.data, fixtures.simple_html)
