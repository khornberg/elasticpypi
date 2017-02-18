simple_html = '<html>\n  <head>\n    <title>Simple Index</title>\n  </head>\n  <body>\n    \n    <a href="/dev/simple/x/">x</a><br/>\n    \n    <a href="/dev/simple/y/">y</a><br/>\n    \n    <a href="/dev/simple/z/">z</a><br/>\n    \n  </body>\n</html>'  # noqa [E501]

links_html = '<html>\n  <head>\n  <title>Links for x</title>\n  </head>\n  <body>\n    <h1>Links for x</h1>\n    \n    <a href="https://">x-0.tar.gz</a></br>\n    \n    <a href="https://">x-1.tar.gz</a></br>\n    \n  </body>\n</html>'  # noqa [E501]

put_event = {
    "Records": [
        {
            "eventVersion": "2.0",
            "eventSource": "aws:s3",
            "awsRegion": "us-west-2",
            "eventTime": "1970-01-01T00:00:00.000Z",
            "eventName": "ObjectCreated:Put",
            "userIdentity": {
                "principalId": "AIDAJDPLRKLG7UEXAMPLE"
            },
            "requestParameters": {
                "sourceIPAddress": "127.0.0.1"
            },
            "responseElements": {
                "x-amz-request-id": "C3D13FE58DE4C810",
                "x-amz-id-2": "FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD"
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "testConfigRule",
                "bucket": {
                    "name": "sourcebucket",
                    "ownerIdentity": {
                        "principalId": "A3NL1KOZZKExample"
                    },
                    "arn": "arn:aws:s3:::sourcebucket"
                },
                "object": {
                    "key": "a-0.tar.gz",
                    "size": 1024,
                    "eTag": "d41d8cd98f00b204e9800998ecf8427e",
                    "versionId": "096fKKXTRTtl3on89fVO.nfljtsv6qko"
                }
            }
        }
    ]
}

delete_event = {
    'Records': [
        {
            "eventVersion": "2.0",
            "eventSource": "aws:s3",
            "awsRegion": "us-west-2",
            "eventTime": "1970-01-01T00:00:00.000Z",
            'eventName': 'ObjectRemoved:Delete',
            "userIdentity": {
                "principalId": "AIDAJDPLRKLG7UEXAMPLE"
            },
            "requestParameters": {
                "sourceIPAddress": "127.0.0.1"
            },
            "responseElements": {
                "x-amz-request-id": "C3D13FE58DE4C810",
                "x-amz-id-2": "FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD"
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "testConfigRule",
                "bucket": {
                    "name": "sourcebucket",
                    "ownerIdentity": {
                        "principalId": "A3NL1KOZZKExample"
                    },
                    "arn": "arn:aws:s3:::sourcebucket"
                },
                "object": {
                    "key": "z-0.tar.gz",
                    "size": 1024,
                    "eTag": "d41d8cd98f00b204e9800998ecf8427e",
                    "versionId": "096fKKXTRTtl3on89fVO.nfljtsv6qko"
                }
            }
        }
    ]
}
