elastic pypi
------------

A fully functional, self-hosted  simple pypi service running on AWS.

# Caveats

**Browse with a browser**
Browsers are currently limited by the removal of basic authentication for remote URLs via the URL (e.g. x:y@z). However, if you visit the URL directly, the browser will prompt you to either enter a username and password, or install this [plugin](https://chrome.google.com/webstore/detail/multipass-for-http-basic/enhldmjbphoeibbpdhmjkchohnidgnah) for Chrome and setup the credentials accordingly.

**Uploads through the api are limited to 6MB**

Uploads are limited to 6MB through the API because Lambda limits the body size. https://docs.aws.amazon.com/lambda/latest/dg/limits.html#limits-list

Uploads directly to the S3 bucket are limited by whatever S3 does.

Only uploads through the API are checked for and discriminated by the `overwrite` configuration setting.

**Downloads are limited to 10MB**

This again is a limitation of AWS; specifically API Gateway.
https://docs.aws.amazon.com/apigateway/latest/developerguide/limits.html#api-gateway-limits

# Setup

1. Edit `serverless.yml`

## Configuration

### serverless.yml

```
service: elasticpypi

provider:
  name: aws
  runtime: python3.9
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
    USERS: "my:blah,your:secret"      # OPTIONAL, default not present
    OVERWRITE: false                  # Allow uploads to overwrite already existing packages
```

#### Users

`USERS` may be a comma delimited string of `username:password`. If present it will be used instead of `USERNAME` and `PASSWORD`

# Deploy

`npm`/`yarn` and `pip` are required to install the necessary packages to deploy.

1. `yarn` or `npm install`
1. `sls deploy`


**Note** that when deploying do not have the virtualenv activated. The `wsgi` plugin for serverless will automatically fetch the python requirements.

# Using

Based on the output of the deploy command or via the AWS console add the url to your pip conf.

The url should be something like `https://blah.execute-api.region.amazonaws.com/dev/simple`.

Make sure you add a trailing slash as required in the PEP.

Make sure you add your basic authentication credentials to your url.

## Throttling

AWS resources could be throttled. As such, if you are intending to dump a bunch of packages into the S3 bucket, please check your
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
        elasticpypi-test

# Changelog
* 2022-05-19 Update serverless and serverless-wsgi versions

* 2022-04-29 Support any cased Authorization header; drop python 3.6 support; updates to a bunch of dependencies

* 2021-03-08 Add Cache-Control header so `pip` caches the package

* 2020-10-12 Multiple users

* 2018-11-26 HTTP Basic Authentication works for in browser browsing

* 2018-01-04 Downloads up to 10 MB work without signed requests

* 2017-12-27 Uploads work. Manually tested with `python setup.py upload` and `twine upload`

* 2017-12-22 Use Python 3, downloads go through the API Gateway so pip's caching now works

* 2017-03-24 The configuration has moved from `./elasticpypi/config.json` to `./serverless.yml` and is consumed by elasticpypi as environment variables. If you are upgrading from an older version, you may need to migrate your configuration to serverless.yml.

