import boto3
from elasticpypi import name
from elasticpypi.config import config

BUCKET = config['bucket']


def get_key(key, full_key):
    if (full_key):
        return key
    return name.compute_package_name(key)


def first_last_capitalize(s):
    return s[:1].upper() + s[1:-1] + s[-1:].upper()


def get_search_string(prefix):
    return "Contents[?starts_with(Key, `{}`) || starts_with(Key, `{}`) || starts_with(Key, `{}`) || starts_with(Key, `{}`)]".format(prefix.capitalize()[:3], prefix.upper()[:3], first_last_capitalize(prefix[:3]), prefix)  # noqa E501


def list_packages(prefix='', full_key=False):
    client = boto3.client('s3')
    packages = set()
    paginator = client.get_paginator('list_objects_v2')
    page_iterator = paginator.paginate(Bucket=BUCKET)
    filtered_iterator = page_iterator.search(get_search_string(prefix))
    for page in filtered_iterator:
        key = page['Key']
        name = get_key(key, full_key)
        if full_key:
            packages.add((signed_url(name), name))
        else:
            packages.add((name, name))
    return sorted(packages)


def exists(filename):
    return len(list_packages(filename, True)) > 0


def download(filename):
    client = boto3.client('s3')
    package = client.get_object(Bucket=BUCKET, Key=filename)
    return package['Body']


def upload(filename, payload):
    client = boto3.client('s3')
    client.upload_fileobj(payload, BUCKET, filename)


def signed_url(filename):
    client = boto3.client('s3')
    url = client.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': filename}, ExpiresIn=5)
    return url
