#!/usr/bin/env bash
set -e

export TABLE=elasticpypi
export USERNAME="$INTERNAL_PYPI_USERNAME"
export PASSWORD="$INTERNAL_PYPI_PASS"
export BUCKET=altitudenetworks-pypi
export FLASK_ENV=development

FLASK_APP=elasticpypi/api.py python -m flask run
