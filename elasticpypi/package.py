from dataclasses import dataclass


@dataclass
class Package:
    package_name: str
    normalized_name: str
    version: str
    download_url: str
