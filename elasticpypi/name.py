"""
From https://github.com/vendasta/cloudpypi/blob/master/cloudpypi/package_api.py#L14
"""
import re

RE_NORMALIZE = re.compile(r"[-_.]+")


def compute_version(package_name: str) -> str:
    return package_name.split("-", 2)[1]


def normalize(package_name: str) -> str:
    package_title = package_name.split("-", 1)[0]
    return RE_NORMALIZE.sub("-", package_title)
