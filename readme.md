elastic pypi
------------

A *mostly* functional simple pypi service running on AWS.

# Caveats

**`python setup.py sdist` does not work**

This is a limitation of AWS API Gateway. There are numerous other ways to upload your packages to the S3 bucket.

**Cannot browse with a browser**

This is a limitation of current browsers. They have removed basic authentication for remote urls via the url (e.g. x:y@z). `WWW-Authenticate` responses do not work with AWS Lambda.

# Setup

1. Copy `elasticpypi/config-example.json` to `elasticpypi/config.json`
1. Edit `config.json`

## Configuration

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

## Using Docker

The example below runs the full test suite. To debug, add `/bin/bash` to the end of the command.

    $ sudo docker build -t elasticpypi-test .
    $ sudo docker run -it \
        -v $(pwd):/code \
        -e AWS_DEFAULT_REGION=artic-1 \
        -e SERVICE=serverless-service-name \
        -e STAGE=/dev \
        -e BUCKET=your-bucket-name \
        -e TABLE=elasticpypi \
        -e USERNAME=elasticpypi \
        -e PASSWORD=something-secretive \
        -e OVERWRITE=false \
        elasticpypi-test


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

# Changelog

* *2017-03-12* The configuration has moved from `./elasticpypi/config.json` to `./serverless.yml` and is consumed by elasticpypi as
environment variables. If you are upgrading from an older version, you may need to migrate your configuration to
serverless.yml.

