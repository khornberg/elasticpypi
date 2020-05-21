import os
import time

import requests
from flask import Flask, Response, abort, redirect, render_template

from elasticpypi.dynamodb_client import DynamoDBClient
from elasticpypi.env_namespace import EnvNamespace
from elasticpypi.s3_client import S3Client

app = Flask(__name__)

PRESIGNED_URL_EXPIRES_IN_SEC = 60 * 60 * 6


@app.route("/simple/")
def simple() -> Response:
    env_namespace = EnvNamespace(os.environ)
    dynamodb_client = DynamoDBClient(env_namespace.table)
    normalized_names = dynamodb_client.list_normalized_names()
    normalized_names.sort()
    return render_template("simple.html", normalized_names=normalized_names)


@app.route("/simple/<normalized_name>/")
def simple_name(normalized_name: str) -> Response:
    env_namespace = EnvNamespace(os.environ)
    dynamodb_client = DynamoDBClient(env_namespace.table)
    packages = dynamodb_client.list_packages_by_name(normalized_name)

    if not packages:
        abort(404)
    return render_template(
        "links.html", packages=packages, normalized_name=normalized_name
    )


def url_needs_update(url):
    if not url:
        return True

    try:
        response = requests.get(url)
    except Exception:
        return True

    if not response.ok:
        return True

    return False


@app.route("/simple/download/<package_name>")
def download(package_name: str) -> Response:
    now = int(time.time())
    env_namespace = EnvNamespace(os.environ)
    dynamodb_client = DynamoDBClient(env_namespace.table)
    package = dynamodb_client.get_item(package_name)
    needs_update = url_needs_update(package.presigned_url)
    if needs_update:
        s3_client = S3Client(env_namespace.bucket)
        package.presigned_url = s3_client.get_presigned_download_url(
            package_name, expires_in=PRESIGNED_URL_EXPIRES_IN_SEC + 60
        )
        package.updated = now
        dynamodb_client.update_item(package)

    response: Response = redirect(package.presigned_url)
    response.cache_control.max_age = (
        PRESIGNED_URL_EXPIRES_IN_SEC + package.updated - now
    )
    response.headers.add_header("x-url-updated", "true" if needs_update else "false")
    return response
