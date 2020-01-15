"""
From https://github.com/vendasta/cloudpypi/blob/master/cloudpypi/package_api.py#L14
"""
import re

RE_NORMALIZE = re.compile(r"[-_.]+")

def compute_version(filename: str) -> str:
    version = filename.split('-', 2)[1]


def normalize(filename: str) -> str:
    # From https://www.python.org/dev/peps/pep-0503/
    return RE_NORMALIZE.sub("-", filename)
