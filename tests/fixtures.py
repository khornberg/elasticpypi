simple_html = '<html>\n  <head>\n    <title>Simple Index</title>\n  </head>\n  <body>\n    \n    <a href="/dev/simple/x/">x</a><br/>\n    \n    <a href="/dev/simple/y/">y</a><br/>\n    \n    <a href="/dev/simple/z/">z</a><br/>\n    \n  </body>\n</html>'  # noqa [E501]

links_html = '<html>\n  <head>\n  <title>Links for x</title>\n  </head>\n  <body>\n    <h1>Links for x</h1>\n    \n    <a href="https://">x-0.tar.gz</a></br>\n    \n    <a href="https://">x-1.tar.gz</a></br>\n    \n  </body>\n</html>'  # noqa [E501]

object_put = {
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
               "key": "HappyFace.jpg",
               "size": 1024,
               "eTag": "d41d8cd98f00b204e9800998ecf8427e",
               "versionId": "096fKKXTRTtl3on89fVO.nfljtsv6qko"
            }
         }
      }
   ]
}

dynamodb_query_django = {
    'Count': 2,
    'Items': [
        {
            'version': '0.1.2',
            'package_name': 'django',
            'filename': 'Django-0.1.2.tar.gz'
        }, {
            'version': '1.8.12',
            'package_name': 'django',
            'filename': 'Django-1.8.12.tar.gz'
        }
    ],
    'ScannedCount': 2,
    'ResponseMetadata': {
        'RetryAttempts': 0,
        'HTTPStatusCode': 200,
        'RequestId': 'MO0',
        'HTTPHeaders': {
            'x-amzn-requestid': 'MO0',
            'content-length': '230',
            'server': 'Server',
            'connection': 'keep-alive',
            'x-amz-crc32': '1604349530',
            'date': 'Thu, 02 Feb 2017 19:45:43 GMT',
            'content-type': 'application/x-amz-json-1.0'
        }
    }
}

dynamodb_query_yapf = {
    'Count': 1,
    'Items': [{
        'version': '0.1.2',
        'package_name': 'yapf',
        'filename': 'yapf-0.1.2.tar.gz'
    }],
    'ScannedCount': 1,
    'ResponseMetadata': {
        'RetryAttempts': 0,
        'HTTPStatusCode': 200,
        'RequestId': 'TVG',
        'HTTPHeaders': {
            'x-amzn-requestid': 'TVG',
            'content-length': '129',
            'server': 'Server',
            'connection': 'keep-alive',
            'x-amz-crc32': '416310657',
            'date': 'Thu, 02 Feb 2017 19:45:43 GMT',
            'content-type': 'application/x-amz-json-1.0'
        }
    }
}
