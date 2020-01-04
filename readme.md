# Elastic PyPI

- [Elastic PyPI](#elastic-pypi)
  - [Fork version differences](#fork-version-differences)
  - [Usage](#usage)
    - [Browser repository](#browser-repository)
    - [Pipfile template](#pipfile-template)
    - [Upload new packages](#upload-new-packages)
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

- Browse [repository](https://078f54k4k0.execute-api.us-west-2.amazonaws.com/dev/simple/) in browser
- `pip`, `pipenv` and `poetry` are supported

### Pipfile template

Add `INTERNAL_PYPI_PASS` env variable to your `~/.bashrc`

```
[[source]]
name = "internal"
url = "https://elasticpypi:${INTERNAL_PYPI_PASS}@078f54k4k0.execute-api.us-west-2.amazonaws.com/dev/simple"
verify_ssl = true

[dev-packages]
pycodestyle = "*"

[packages]
my-package = {path = ".",editable = true}

[requires]
python_version = "3.7"
```

### Upload new packages

First, make sure you have [deployment_tools](https://github.com/altitudenetworks/deployment_tools) in your repo.

- To add a new dependency or a dev dependency, use `pypi_upload my_dependency==1.2.3 && pipenv install my_dependency==1.2.3`
- Upload all requirements for your package `pypi_upload --requirements`
- Upload new version of your package `pypi_upload --release`

## Deploy

[yarn](https://yarnpkg.com/lang/en/) is required to install the necessary packages to deploy.

- `yarn install`
- `yarn run sls deploy --password ${INTERNAL_PYPI_PASS}`


**Note** that when deploying do not have the virtualenv activated. The `wsgi` plugin for serverless will automatically fetch the python requirements.

### Throttling

AWS resources could be throttled. As such, if you are intending to dump a bunch of packages into the S3 bucket, please check your
service and account limits. Additionally, changing the read and write capacity of dynamodb may help. It is currently set
to the lowest possible unit (1).
