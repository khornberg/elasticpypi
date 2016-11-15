import boto3
from elasticpypi import name
from elasticpypi.config import config

BUCKET = config['bucket']


def get_key(key, full_key):
    if (full_key):
        return key
    return name.compute_package_name(key)


def first_last_capitalize(prefix):
    return prefix[:1].upper() + prefix[1:-1] + prefix[-1:].upper()


def underscores(prefix):
    """
    Bluntly replace dashes with underscores for those packages that use underscores
    """
    return prefix.replace('-', '_')


def third_capitalize(prefix):
    return prefix[:-1] + prefix[-1:].upper()


def get_search_string(prefix):
    return "Contents[?{}]".format(get_permutations(prefix))


def get_permutations(prefix):
    pre = prefix[:3]
    return " || ".join(
        (
            "starts_with(Key, `{}`)".format(x)
            for x in
            [pre.capitalize(), pre.upper(), first_last_capitalize(pre), underscores(prefix), third_capitalize(pre)]
        )
    )


def get_packages_by_prefix(paginator, prefix, full_key):
    packages = set()
    page_iterator = paginator.paginate(Bucket=BUCKET, Prefix=prefix)
    for page in page_iterator:
        if 'Contents' in page:
            for key in page['Contents']:
                key = key['Key']
                name = get_key(key, full_key)
                if full_key:
                    if get_key(key, False) == prefix:
                        packages.add((signed_url(name), name))
                else:
                    packages.add((name, name))
    return packages


def get_packages_by_jmespath(paginator, prefix, full_key):
    packages = set()
    page_iterator = paginator.paginate(Bucket=BUCKET)
    filtered_iterator = page_iterator.search(get_search_string(prefix))
    for page in filtered_iterator:
        key = page['Key']
        name = get_key(key, full_key)
        if full_key:
            packages.add((signed_url(name), name))
        else:
            packages.add((name, name))
    return packages


def list_packages(prefix='', full_key=False):
    client = boto3.client('s3')
    paginator = client.get_paginator('list_objects_v2')
    packages = get_packages_by_prefix(paginator, prefix, full_key)
    if not len(packages):
        packages = get_packages_by_jmespath(paginator, prefix, full_key)
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
    url = client.generate_presigned_url('get_object', Params={'Bucket': BUCKET, 'Key': filename}, ExpiresIn=15)
    return url
