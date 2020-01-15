from flask import Flask
from flask import render_template
from flask import request
from flask import abort

from elasticpypi.dynamodb import DynamoDBClient
from elasticpypi.config import config

app = Flask(__name__)


@app.route("/simple/")
def simple():
    dynamodb_client = DynamoDBClient()
    prefixes = dynamodb_client.list_packages()
    return render_template("simple.html", prefixes=prefixes, stage=config["stage"])


@app.route("/simple/<normalized_name>/")
def simple_name(normalized_name):
    dynamodb_client = DynamoDBClient()
    packages = dynamodb_client.list_packages_by_name(normalized_name)
    if not packages:
        abort(404)
    return render_template(
        "links.html",
        packages=packages,
        normalized_name=normalized_name,
        stage=config["stage"],
    )
