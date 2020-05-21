from dataclasses import dataclass


@dataclass
class Package:
    name: str
    normalized_name: str
    version: str
    sha256: str
    presigned_url: str
    presigned_url_expires: int
