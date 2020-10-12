from unittest import TestCase
from tests.fixtures import typical_request
from elasticpypi.handler import auth


class AuthTests(TestCase):

    def test_auth_can_decode_basic_auth_header(self):
        expected = {
            'principalId': 'elasticpypi',
            'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                    {
                        'Action': 'execute-api:Invoke',
                        'Effect': 'Allow',
                        'Resource': ['arn:aws:execute-api:us-artic-1:1234567890:*/packages/*/*']
                    }
                ]
            }
        }
        policy_document = auth(typical_request(), {})
        self.maxDiff = None
        self.assertEqual(policy_document, expected)

    def test_auth_raises_401_when_comparison_fails(self):
        with self.assertRaises(Exception):
            auth(typical_request(password='notCorrect'), {})
