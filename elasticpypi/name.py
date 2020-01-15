import re

RE_PACKAGE_NAME = re.compile(r"^(?P<name>.+)-(?P<version>\d+(\.\d+[^-.]*)+)")


def compute_version(package_name: str) -> str:
    match = RE_PACKAGE_NAME.match(package_name)
    if not match:
        raise ValueError(f"Wrong package name format: {package_name}")

    return match.group("version")


def normalize(package_name: str) -> str:
    match = RE_PACKAGE_NAME.match(package_name)
    if not match:
        raise ValueError(f"Wrong package name format: {package_name}")

    return match.group("name")
