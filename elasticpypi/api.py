import boto3
from flask import Flask
from flask import send_file
from flask import render_template
from elasticpypi.auth import requires_auth
from elasticpypi import s3, dynamodb
from elasticpypi.config import config

app = Flask(__name__)


@app.route("/simple/")
@requires_auth
def simple():
    db = boto3.resource('dynamodb')
    prefixes = dynamodb.list_packages(db)
    return render_template('simple.html', prefixes=prefixes, stage=config['stage'])


@app.route('/simple/<name>/')
@requires_auth
def simple_name(name):
    db = boto3.resource('dynamodb')
    packages = dynamodb.list_packages_by_name(db, name)
    return render_template('links.html', packages=packages, package=name, stage=config['stage'])


@app.route('/packages/<name>')
@requires_auth
def packages_name(name):
    fp = s3.download(name)
    return send_file(fp, as_attachment=True, attachment_filename=name)
