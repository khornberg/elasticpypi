import boto3
from flask import Flask
from flask import render_template
from flask import request
from flask import abort
from elasticpypi import s3, dynamodb
from elasticpypi.config import config

app = Flask(__name__)


@app.route("/simple/", methods=["GET", "POST"])
def simple():
    if request.method == "POST":
        f = request.files["content"]
        if "/" in f.filename:
            abort(400)
        if config["overwrite"] == "false" and dynamodb.exists(f.filename):
            abort(409)
        s3.upload(f.filename, f.stream)
        return "", 200
    db = boto3.resource("dynamodb")
    prefixes = dynamodb.list_packages(db)
    return render_template("simple.html", prefixes=prefixes, stage=config["stage"])


@app.route("/simple/<name>/")
def simple_name(name):
    db = boto3.resource("dynamodb")
    packages = dynamodb.list_packages_by_name(db, name)
    return render_template("links.html", packages=packages, package=name, stage=config["stage"])
