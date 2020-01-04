# Elastic PyPI

- [Elastic PyPI](#elastic-pypi)
  - [Fork version differences](#fork-version-differences)
  - [Usage](#usage)
    - [Browser repository](#browser-repository)
  - [Deploy](#deploy)
    - [Throttling](#throttling)

A fully functional, self-hosted simple pypi service running on AWS.

## Fork version differences

- `serverless.yml` has config for AltitudeNetworks
- Packages download from S3 presigned URLs to remove 10 MB download limit for API Gateway
- Fixed package links in GUI
- Missing packages return 404 status code instead of a page with no links
- Fixed S3 delete trigger

## Usage

### Browser repository

- Browse repository in browser
- `pip`, `pipenv` and `poetry` are supported

## Deploy

[yarn](https://yarnpkg.com/lang/en/) is required to install the necessary packages to deploy.

- `yarn install`
- `yarn run sls deploy --password ${INTERNAL_PYPI_PASS}`


**Note** that when deploying do not have the virtualenv activated. The `wsgi` plugin for serverless will automatically fetch the python requirements.

### Throttling

AWS resources could be throttled. As such, if you are intending to dump a bunch of packages into the S3 bucket, please check your
service and account limits. Additionally, changing the read and write capacity of dynamodb may help. It is currently set
to the lowest possible unit (1).
