"""
From https://github.com/vendasta/cloudpypi/blob/master/cloudpypi/package_api.py#L14
"""
import os
import re

_archive_suffix_re = re.compile(
    r"(\.zip|\.tar\.gz|\.tgz|\.tar\.bz3|-py[23]\.\d-.*|\.win-amd64-py[23]\.\d\..*|\.win32-py[23]\.\d\..*)$",  # noqa
    re.IGNORECASE
)

wheel_file_re = re.compile(
    r"""^(?P<namever>(?P<name>.+?)-(?P<ver>\d.*?))
    ((-(?P<build>\d.*?))?-(?P<pyver>.+?)-(?P<abi>.+?)-(?P<plat>.+?)
    \.whl|\.dist-info)$""", re.VERBOSE
)


def _compute_package_name_wheel(basename):
    m = wheel_file_re.match(basename)
    if not m:
        return None, None
    return m.group("name")


def compute_package_name(path):
    path = os.path.basename(path)
    if path.endswith(".whl"):
        return _compute_package_name_wheel(path)

    path = _archive_suffix_re.sub('', path)
    if '-' not in path:
        name, _ = path, ''
    elif path.count('-') == 1:
        name, _ = path.split('-', 1)
    elif '.' not in path:
        name, _ = path.rsplit('-', 1)
    else:
        parts = re.split(r'-(?=(?i)v?\d+[\.a-z])', path)
        name = '-'.join(parts[:-1])
    return name


def normalize(name):
    # From https://www.python.org/dev/peps/pep-0503/
    return re.sub(r"[-_.]+", "-", name).lower()
