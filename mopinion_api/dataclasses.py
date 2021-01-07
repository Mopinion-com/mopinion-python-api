import re

from dataclasses import dataclass
from mopinion_api import settings


@dataclass(frozen=True)
class Credentials:
    public_key: str
    private_key: str


@dataclass(frozen=True)
class Version:
    name: str = settings.VERSION

    def __post_init__(self):
        if self.name not in settings.VERSIONS:
            raise ValueError(
                f"'{self.name}' is not a valid version. Please consider one of: "
                f"'{''.join(settings.VERSIONS)}'"
            )


@dataclass(frozen=True)
class ContentNegotiation:
    name: str = "application/json"

    def __post_init__(self):
        if self.name not in settings.CONTENT_NEGOTIATIONS:
            raise ValueError(
                f"'{self.name}' is not a valid content negotiation. "
                f"Please consider one of: '{', '.join(settings.CONTENT_NEGOTIATIONS)}'"
            )


@dataclass(frozen=True)
class Verbosity:
    name: str = settings.VERBOSITY

    def __post_init__(self):
        if self.name not in settings.VERBOSITY_lEVELS:
            raise ValueError(
                f"'{self.name}' is not a valid verbosity level. Please consider one of: "
                f"'{', '.join(settings.VERBOSITY_lEVELS)}'"
            )


@dataclass(frozen=True)
class Method:
    name: str = "/accounts"

    def __post_init__(self):
        if self.name.lower() not in settings.ALLOWED_METHODS:
            raise ValueError(
                f"'{self.name}' is not a valid choice. Please consider one of: "
                f"'{', '.join(settings.ALLOWED_METHODS)}'"
            )


@dataclass(frozen=True)
class EndPoint:
    name: str

    def __post_init__(self):
        if not self.name.startswith("/"):
            raise ValueError("Endpoint must start with '/'")

        regexps = [
            r"/token$",
            r"/ping$",
            r"/account$",
            r"/deployments$",
            r"/deployments/\w+$",
            r"/datasets$",
            r"/datasets/[-+]?[0-9]+$",
            r"/datasets/[-+]?[0-9]+/fields$",
            r"/reports/[-+]?[0-9]+/fields$",
            r"/datasets/int/feedback/\w+$",
            r"/reports/[-+]?[0-9]+/feedback/\w+",
            r"/reports/[-+]?[0-9]+$",
            r"/reports$",
        ]
        regexp = re.compile('|'.join(regexps), re.IGNORECASE)
        if not regexp.search(self.name):
            raise ValueError(f"Resource '{self.name}' is not supported.")
