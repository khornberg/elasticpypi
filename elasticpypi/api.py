import os

from flask import Flask, Response, abort, redirect, render_template, send_file

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
    s3_object = s3_client.get_object(package_name)
    presigned_url = s3_client.get_presigned_download_url(package_name)
    response: Response = redirect(presigned_url, code=301)
    response.cache_control.max_age = 365000000
    response.set_etag(s3_object["ETag"].replace('"', ""))
    response.content_length = s3_object["ContentLength"]
    response.last_modified = s3_object["LastModified"]
    return response
