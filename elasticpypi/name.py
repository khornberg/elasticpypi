import os.path
from typing import Tuple

from packaging.utils import canonicalize_name
from packaging.version import InvalidVersion, Version

EXTENSIONS = (".tar", ".gz", ".bz", ".whl", ".zip")


def get_parts(package_name: str) -> Tuple[str, str]:
    while os.path.splitext(package_name)[-1].lower() in EXTENSIONS:
        package_name = os.path.splitext(package_name)[0]

    parts = package_name.split("-")
    while parts:
        last_part = parts[-1]
        if last_part and last_part[0].isdigit():
            version_str = parts.pop()
            try:
                version_str = str(Version(version_str))
            except InvalidVersion:
                pass
            return (canonicalize_name("-".join(parts)), version_str)

        parts.pop()

    return (canonicalize_name(package_name), "0.0.0")


def normalize_version(package_name: str) -> str:
    return get_parts(package_name)[-1]


def normalize_name(package_name: str) -> str:
    return get_parts(package_name)[0]
