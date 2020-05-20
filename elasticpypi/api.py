import os

from flask import Flask, Response, abort, redirect, render_template

from elasticpypi.dynamodb_client import DynamoDBClient
from elasticpypi.env_namespace import EnvNamespace
from elasticpypi.s3_client import S3Client

app = Flask(__name__)


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


@app.route("/simple/download/<package_name>")
def download(package_name: str) -> Response:
    env_namespace = EnvNamespace(os.environ)
    s3_client = S3Client(env_namespace.bucket)
    dynamodb_client = DynamoDBClient(env_namespace.table)
    package = dynamodb_client.get_item(package_name)
    response: Response = redirect(s3_client.get_presigned_download_url(package_name))
    if package.sha256:
        response.set_etag(package.sha256)
    return response
