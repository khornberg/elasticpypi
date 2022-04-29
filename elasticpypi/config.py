import os

WATCHED = [
    "SERVICE",
    "STAGE",
    "BUCKET",
    "TABLE",
    "OVERWRITE",
    "USERS",
]

# load config
_config = {k.lower(): v for k, v in os.environ.items() if k in WATCHED}
if not _config.get("users"):
    _config["username"] = os.environ.get("USERNAME")
    _config["password"] = os.environ.get("PASSWORD")
config = _config
