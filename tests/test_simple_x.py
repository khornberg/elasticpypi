import re
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
        self.headers = {'Authorization': 'Basic ' + b64encode("{0}:{1}".format(username, password))}

    def test_get_simple_x_401(self):
        response = self.client.get('/simple/x/')
        self.assert401(response)

    @mock_dynamodb2
    def test_get_simple_x_200_from_dynamodb(self):
        mock_dynamodb_table.make_table([
            {
                'package_name': 'z',
                'version': '0',
                'normalized_name': 'z',
                'filename': 'x-0.tar.gz'
            }, {
                'package_name': 'y',
                'version': '0',
                'normalized_name': 'y',
                'filename': 'x-0.tar.gz'
            }, {
                'package_name': 'x',
                'version': '0',
                'normalized_name': 'x',
                'filename': 'x-0.tar.gz'
            }, {
                'package_name': 'x',
                'version': '1',
                'normalized_name': 'x',
                'filename': 'x-1.tar.gz'
            }
        ])
        response = self.client.get('/simple/x/', headers=self.headers)
        html = re.sub("href=\"https://.*\"", "href=\"https://\"", response.data)  # Remove signed url since it changes
        self.assert200(response)
        self.assertEqual(html, fixtures.links_html)
