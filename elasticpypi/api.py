from flask import Flask
from flask import render_template
from flask import request
from flask import abort

from elasticpypi.dynamodb import DynamoDBClient
from elasticpypi.s3 import S3Client
from elasticpypi.config import config

app = Flask(__name__)


@app.route("/simple/", methods=["GET", "POST"])
def simple():
    dynamodb_client = DynamoDBClient()
    if request.method == "POST":
        f = request.files["content"]
        if "/" in f.filename:
            abort(400)
        if config["overwrite"] == "false" and dynamodb_client.exists(f.filename):
            abort(409)
        S3Client().upload(f.filename, f.stream)
        return "", 200
    prefixes = dynamodb_client.list_packages()
    return render_template("simple.html", prefixes=prefixes, stage=config["stage"])


@app.route("/simple/<name>/")
def simple_name(name):
    dynamodb_client = DynamoDBClient()
    packages = dynamodb_client.list_packages_by_name(name)
    if not packages:
        abort(404)
    return render_template(
        "links.html", packages=packages, package=name, stage=config["stage"]
    )
