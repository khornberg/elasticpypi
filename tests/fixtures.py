from basicauth import encode

simple_html = '<html>\n  <head>\n    <title>Simple Index</title>\n  </head>\n  <body>\n    \n    <a href="/dev/simple/x/">x</a><br/>\n    \n    <a href="/dev/simple/y/">y</a><br/>\n    \n    <a href="/dev/simple/z/">z</a><br/>\n    \n  </body>\n</html>'  # noqa [E501]

links_html = '<html>\n  <head>\n  <title>Links for x</title>\n  </head>\n  <body>\n    <h1>Links for x</h1>\n    \n    <a href="/dev/packages/x-0.tar.gz">x-0.tar.gz</a></br>\n    \n    <a href="/dev/packages/x-1.tar.gz">x-1.tar.gz</a></br>\n    \n  </body>\n</html>'  # noqa [E501]

wheel_links_html = '<html>\n  <head>\n  <title>Links for curses</title>\n  </head>\n  <body>\n    <h1>Links for curses</h1>\n    \n    <a href="/dev/packages/curses-2.2-cp36-cp36m-win_amd64.whl">curses-2.2-cp36-cp36m-win_amd64.whl</a></br>\n    \n  </body>\n</html>'  # noqa [E501]


def put_event(package_name="a+b-0.tar.gz"):
    return {
        "Records": [
            {
                "eventVersion": "2.0",
                "eventSource": "aws:s3",
                "awsRegion": "us-west-2",
                "eventTime": "1970-01-01T00:00:00.000Z",
                "eventName": "ObjectCreated:Put",
                "userIdentity": {"principalId": "AIDAJDPLRKLG7UEXAMPLE"},
                "requestParameters": {"sourceIPAddress": "127.0.0.1"},
                "responseElements": {
                    "x-amz-request-id": "C3D13FE58DE4C810",
                    "x-amz-id-2": "FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD",
                },
                "s3": {
                    "s3SchemaVersion": "1.0",
                    "configurationId": "testConfigRule",
                    "bucket": {
                        "name": "sourcebucket",
                        "ownerIdentity": {"principalId": "A3NL1KOZZKExample"},
                        "arn": "arn:aws:s3:::sourcebucket",
                    },
                    "object": {
                        "key": package_name,
                        "size": 1024,
                        "eTag": "d41d8cd98f00b204e9800998ecf8427e",
                        "versionId": "096fKKXTRTtl3on89fVO.nfljtsv6qko",
                    },
                },
            }
        ]
    }


put_event_for_wheel = {
    "Records": [
        {
            "eventVersion": "2.0",
            "eventSource": "aws:s3",
            "awsRegion": "us-west-2",
            "eventTime": "1970-01-01T00:00:00.000Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {"principalId": "AIDAJDPLRKLG7UEXAMPLE"},
            "requestParameters": {"sourceIPAddress": "127.0.0.1"},
            "responseElements": {
                "x-amz-request-id": "C3D13FE58DE4C810",
                "x-amz-id-2": "FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD",
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "testConfigRule",
                "bucket": {
                    "name": "sourcebucket",
                    "ownerIdentity": {"principalId": "A3NL1KOZZKExample"},
                    "arn": "arn:aws:s3:::sourcebucket",
                },
                "object": {
                    "key": "z-0-cp34-cp34m-manylinux1_x86_64.whl",
                    "size": 1024,
                    "eTag": "d41d8cd98f00b204e9800998ecf8427e",
                    "versionId": "096fKKXTRTtl3on89fVO.nfljtsv6qko",
                },
            },
        }
    ]
}

delete_event = {
    "Records": [
        {
            "eventVersion": "2.0",
            "eventSource": "aws:s3",
            "awsRegion": "us-west-2",
            "eventTime": "1970-01-01T00:00:00.000Z",
            "eventName": "ObjectRemoved:Delete",
            "userIdentity": {"principalId": "AIDAJDPLRKLG7UEXAMPLE"},
            "requestParameters": {"sourceIPAddress": "127.0.0.1"},
            "responseElements": {
                "x-amz-request-id": "C3D13FE58DE4C810",
                "x-amz-id-2": "FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD",
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "testConfigRule",
                "bucket": {
                    "name": "sourcebucket",
                    "ownerIdentity": {"principalId": "A3NL1KOZZKExample"},
                    "arn": "arn:aws:s3:::sourcebucket",
                },
                "object": {
                    "key": "z-0.tar.gz",
                    "size": 1024,
                    "eTag": "d41d8cd98f00b204e9800998ecf8427e",
                    "versionId": "096fKKXTRTtl3on89fVO.nfljtsv6qko",
                },
            },
        }
    ]
}


def typical_request(user="elasticpypi", password="something-secretive"):
    authorization = encode(user, password)
    return {
        "resource": "/",
        "path": "/",
        "httpMethod": "GET",
        "methodArn": "arn:aws:execute-api:us-artic-1:1234567890:lttrsNmbrs/packages/GET/",
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4",
            "Authorization": "{}".format(authorization),
            "cache-control": "max-age=0",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "GB",
            "content-type": "application/x-www-form-urlencoded",
            "Host": "j3ap25j034.execute-api.eu-west-2.amazonaws.com",
            "origin": "https://j3ap25j034.execute-api.eu-west-2.amazonaws.com",
            "Referer": "https://j3ap25j034.execute-api.eu-west-2.amazonaws.com/dev/",
            "upgrade-insecure-requests": "1",
            "User-Agent": "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
            "Via": "2.0 a3650115c5e21e2b5d133ce84464bea3.cloudfront.net (CloudFront)",
            "X-Amz-Cf-Id": "0nDeiXnReyHYCkv8cc150MWCFCLFPbJoTs1mexDuKe2WJwK5ANgv2A==",
            "X-Amzn-Trace-Id": "Root=1-597079de-75fec8453f6fd4812414a4cd",
            "X-Forwarded-For": "50.129.117.14, 50.112.234.94",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "queryStringParameters": None,
        "pathParameters": None,
        "stageVariables": None,
        "requestContext": {
            "path": "/dev/",
            "accountId": "124062937612",
            "resourceId": "qdolsr1yhk",
            "stage": "dev",
            "requestId": "0f2431a2-6d2f-11e7-b75152aa497861",
            "identity": {
                "cognitoIdentityPoolId": None,
                "accountId": None,
                "cognitoIdentityId": None,
                "caller": None,
                "apiKey": "",
                "sourceIp": "50.129.117.14",
                "accessKey": None,
                "cognitoAuthenticationType": None,
                "cognitoAuthenticationProvider": None,
                "userArn": None,
                "userAgent": "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
                "user": None,
            },
            "resourcePath": "/",
            "httpMethod": "GET",
            "apiId": "j3azlsj0c4",
        },
        "body": "postcode=LS17FR",
        "isBase64Encoded": False,
    }
