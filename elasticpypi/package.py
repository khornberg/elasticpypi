from dataclasses import dataclass, field
import time


@dataclass
class Package:
    name: str
    normalized_name: str
    version: str
    sha256: str
    presigned_url: str
    updated: int
