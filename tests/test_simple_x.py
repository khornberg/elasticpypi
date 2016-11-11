from flask_testing import TestCase
from base64 import b64encode
import mock
from elasticpypi.api import app
from elasticpypi.config import config
from tests import fixtures


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

    @mock.patch('elasticpypi.s3.signed_url')
    @mock.patch('elasticpypi.s3.list_packages')
    def test_get_simple_x_200(self, list_packages, signed_url):
        list_packages.return_value = [('https://xyz', 'x-0.3.3.tar.gz'), ('https://xyz', 'x-1.1.1.tar.gz')]
        response = self.client.get('/simple/x/', headers=self.headers)
        self.assert200(response)
        self.assertEqual(response.data, fixtures.links_html)
        list_packages.assert_called_with('x', True)
