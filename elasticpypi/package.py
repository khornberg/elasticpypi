from dataclasses import dataclass


@dataclass
class Package:
    name: str
    normalized_name: str
    version: str
    sha256: str
