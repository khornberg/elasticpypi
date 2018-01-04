from flask_testing import TestCase
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
        response = self.client.get('/simple/x/')
        self.assert200(response)
        self.assertEqual(response.data.decode(), fixtures.links_html)
