import json
from flask_testing import TestCase
from elasticpypi.api import app
from elasticpypi.config import config
from moto import mock_dynamodb2
from tests import mock_dynamodb_table

TABLE = config['table']


class JsonProjectTests(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_wrong_content_type(self):
        response = self.client.get('/pypi/y/json', content_type='text/plain')
        self.assertEqual(response.status_code, 415)

    @mock_dynamodb2
    def test_get_json_for_project(self):
        mock_dynamodb_table.make_table(
            items=[
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
                    'package_name': 'x-1.1.whl',
                    'version': '1.1',
                    'normalized_name': 'x',
                    'filename': 'x-1.1.whl'
                }, {
                    'package_name': 'x-0.1.whl',
                    'version': '0.1',
                    'normalized_name': 'x',
                    'filename': 'x-0.1.whl'
                }, {
                    'package_name': 'x-1.tar.gz',
                    'version': '1',
                    'normalized_name': 'x',
                    'filename': 'x-1.tar.gz'
                }, {
                    'package_name': 'x-1.1.tar.gz',
                    'version': '1.1',
                    'normalized_name': 'x',
                    'filename': 'x-1.1.tar.gz'
                }
            ]
        )
        response = self.client.get('/pypi/x/json', content_type='application/json')
        self.assert200(response)
        expected = {
            'info': {
                'name': 'x'
            },
            'last_serial': None,
            'releases': {
                '0': [{
                    'filename': 'x-0.tar.gz',
                    'url': '/dev/packages/x-0.tar.gz'
                }],
                '0.1': [{
                    'filename': 'x-0.1.whl',
                    'url': '/dev/packages/x-0.1.whl'
                }],
                '1': [{
                    'filename': 'x-1.tar.gz',
                    'url': '/dev/packages/x-1.tar.gz'
                }],
                '1.1': [
                    {
                        'filename': 'x-1.1.tar.gz',
                        'url': '/dev/packages/x-1.1.tar.gz'
                    }, {
                        'filename': 'x-1.1.whl',
                        'url': '/dev/packages/x-1.1.whl'
                    }
                ]
            },
            'urls': [
                {
                    'filename': 'x-1.1.tar.gz',
                    'url': '/dev/packages/x-1.1.tar.gz'
                }, {
                    'filename': 'x-1.1.whl',
                    'url': '/dev/packages/x-1.1.whl'
                }
            ]
        }
        self.assertEqual(json.loads(response.data.decode()), expected)
