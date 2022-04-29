import pytest
from tests.fixtures import typical_request
from elasticpypi.handler import auth


def test_authorization_header_can_be_mixed_case():
    expected = {
        "principalId": "elasticpypi",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": ["arn:aws:execute-api:us-artic-1:1234567890:*/packages/*/*"],
                }
            ],
        },
    }
    request_event = typical_request()
    request_event["headers"]["authorization"] = request_event["headers"]["Authorization"]
    del request_event["headers"]["Authorization"]
    policy_document = auth(request_event, {})
    assert policy_document == expected


def test_auth_can_decode_basic_auth_header_for_users():
    expected = {
        "principalId": "elasticpypi",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": ["arn:aws:execute-api:us-artic-1:1234567890:*/packages/*/*"],
                }
            ],
        },
    }
    policy_document = auth(typical_request(), {})
    assert policy_document == expected
    policy_document = auth(typical_request(user="user2", password="blah"), {})
    expected["principalId"] = "user2"
    assert policy_document == expected


# This test is order dependent because the config is modified
def test_get_username_and_password_form_environment():
    from elasticpypi import config

    del config.config["users"]
    config.config["username"] = "user3"
    config.config["password"] = "blah"
    expected = {
        "principalId": "user3",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": ["arn:aws:execute-api:us-artic-1:1234567890:*/packages/*/*"],
                }
            ],
        },
    }
    policy_document = auth(typical_request(user="user3", password="blah"), {})
    assert policy_document == expected


def test_auth_raises_401_when_comparison_fails():
    with pytest.raises(Exception):
        auth(typical_request(password="notCorrect"), {})
