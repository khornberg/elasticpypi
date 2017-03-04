elastic pypi
------------

A *mostly* functional simple pypi service running on AWS.

# Caveats

**Uploads do not work**

This is a limitation of AWS API Gateway. You will have to find other ways to upload your packages to the S3 bucket.

Running `serverless wsgi` locally allows uploads to work.

**Cannot browse with a browser**

This is a limitation of current browsers. They have removed basic authentication for remote urls via the url (e.g. x:y@z). `WWW-Authenticate` responses do not work with AWS Lambda.

# Setup

1. Copy `elasticpypi/config-example.json` to `elasticpypi/config.json`
1. Edit `config.json`

## Configuration

### Warning for Upgraders!

The configuration now lives in serverless.yml and is consumed by elasticpypi as environment variables. If you are
upgrading, you will need to move your configuration from config.json to serverless.yml.

### serverless.yml

```
service: elasticpypi

provider:
  name: aws
  runtime: python2.7
  memorySize: 128
  stage: dev
  # profile: "some-local-aws-config-profile"
  # region: us-east-1

  environment:
    SERVICE: ${self:service}          # See above. Defaults to elasticpypi
    STAGE: "/${self:provider.stage}"  # See above. Defaults to dev
    BUCKET: "elasticpypi"             # CHANGE ME
    TABLE: "elasticpypi"              # You can change me if you want, but do you?
    USERNAME: "elasticpypi"           # You can change me if you want, but do you?
    PASSWORD: "something-secretive"   # CHANGE ME
    OVERWRITE: false                  # Only applies to the local server.
                                      # If true will overwrite packages
```

# Deploy

`yarn` and `pip` are required to install the necessary packages to deploy.

1. `yarn`
1. `sls deploy`


**Note** that when deploying do not have the virtualenv activated. The `wsgi` plugin for serverless will automatically fetch the python requirements.

# Using

Based on the output of the deploy command or via the AWS console add the url to your pip conf.

The url should be something like `https://blah.execute-api.region.amazonaws.com/dev/simple`.

Make sure you add a trailing slash as required in the PEP.

Make sure you add your basic authentication credentials to your url.

## Throttling

AWS resources maybe throttled. As such, if you are intending to dump a bunch of packages into the S3 bucket check your
service and account limits. Additionally, changing the read and write capacity of dynamodb may help. It is currently set
to the lowest possible unit (1).

# Testing

## Requirements

1. Install testing requirements from `test-requirements.txt`
1. Run `python -m pytest`

## docker-test.sh

If you have Docker installed, try the script. For example, this will build the Docker image, run the tests and start an
interactive container.

    $ ./docker-test.sh build test debug

### Usage

    $ ./docker-test.sh help
    run this from inside your elasticpypi repo dir.
    options:
      build  - Builds the Dockerfile before running tests.
      test   - Runs tests inside a Docker container
      debug  - Runs bash in an interactive Docker container
               with `pwd` mounted at /code

# Todo

1. Proxy for packages not found
1. Token auth of some kind for browsing in a browser
