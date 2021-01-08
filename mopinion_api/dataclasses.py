import re

from dataclasses import dataclass, field
from mopinion_api import settings


class Argument:
    pass


class ResourceArgument:
    pass


@dataclass(frozen=True)
class Credentials(Argument):
    public_key: str
    private_key: str


@dataclass(frozen=True)
class Version(Argument):
    name: str = settings.VERSION

    def __post_init__(self):
        if self.name not in settings.VERSIONS:
            raise ValueError(
                f"'{self.name}' is not a valid version. Please consider one of: "
                f"'{''.join(settings.VERSIONS)}'"
            )


@dataclass(frozen=True)
class ContentNegotiation(Argument):
    name: str = "application/json"

    def __post_init__(self):
        if self.name not in settings.CONTENT_NEGOTIATIONS:
            raise ValueError(
                f"'{self.name}' is not a valid content negotiation. "
                f"Please consider one of: '{', '.join(settings.CONTENT_NEGOTIATIONS)}'"
            )


@dataclass(frozen=True)
class Verbosity(Argument):
    name: str = settings.VERBOSITY

    def __post_init__(self):
        if self.name.lower() not in settings.VERBOSITY_lEVELS:
            raise ValueError(
                f"'{self.name}' is not a valid verbosity level. Please consider one of: "
                f"'{', '.join(settings.VERBOSITY_lEVELS)}'"
            )


@dataclass(frozen=True)
class Method(Argument):
    name: str = "GET"

    def __post_init__(self):
        if self.name.lower() not in settings.ALLOWED_METHODS:
            raise ValueError(
                f"'{self.name}' is not a valid choice. Please consider one of: "
                f"'{', '.join(settings.ALLOWED_METHODS)}'"
            )


@dataclass(frozen=True)
class EndPoint(Argument):
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
        regexp = re.compile("|".join(regexps), re.IGNORECASE)
        if not regexp.search(self.name):
            raise ValueError(f"Resource '{self.name}' is not supported.")


@dataclass(frozen=True)
class ResourceVerbosity(ResourceArgument):
    name: str = settings.VERBOSITY
    iterate: bool = False

    def __post_init__(self):
        # if we want to iterate we need metadata, verbosity higher or equal than normal
        if self.iterate and self.name.lower() not in settings.ITERATE_VERBOSITY_lEVELS:
            raise ValueError(
                f"'{self.name}' is not a valid verbosity level. Please consider one of: "
                f"'{', '.join(settings.ITERATE_VERBOSITY_lEVELS)}'"
            )


@dataclass
class ResourceUri(ResourceArgument):
    name: str = field(init=False)
    resource_name: str
    resource_id: str
    sub_resource_name: str
    sub_resource_id: str

    def __post_init__(self):
        uri = self.resource_name
        if self.resource_id:
            uri += f"/{self.resource_id}"
            if self.sub_resource_name:
                uri += f"/{self.sub_resource_name}"
                if self.sub_resource_id:
                    uri += f"/{self.sub_resource_id}"
        self.name = uri
