from typing import Dict


class EnvError(Exception):
    pass


class EnvNamespace:
    def __init__(self, environ: Dict[str, str]) -> None:
        self.environ = environ

    def _get_required(self, key: str) -> str:
        try:
            return self.environ[key]
        except KeyError:
            raise EnvError(f"{key} env variable is not set")

    @property
    def service(self) -> str:
        return self._get_required("SERVICE")

    @property
    def stage(self) -> str:
        return self._get_required("STAGE")

    @property
    def bucket(self) -> str:
        return self._get_required("BUCKET")

    @property
    def table(self) -> str:
        return self._get_required("TABLE")

    @property
    def username(self) -> str:
        return self._get_required("USERNAME")

    @property
    def password(self) -> str:
        return self._get_required("PASSWORD")

    @property
    def overwrite(self) -> bool:
        return self._get_required("OVERWRITE") == "true"
