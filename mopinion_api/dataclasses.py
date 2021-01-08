import re

from dataclasses import dataclass, field
from mopinion_api import settings
from typing import Optional, Union


class Argument:
    pass


@dataclass(frozen=True)
class Credentials(Argument):
    public_key: str
    private_key: str


@dataclass(frozen=True)
class Endpoint(Argument):
    path: str

    def __post_init__(self):
        # endpoint must start with '/'
        if not self.path.startswith("/"):
            raise ValueError("Endpoint must start with '/'")

        # endpoint must be one of these
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
            r"/datasets/[-+]?[0-9]+/feedback/\w+$",
            r"/reports/[-+]?[0-9]+/feedback/\w+",
            r"/reports/[-+]?[0-9]+$",
            r"/reports$",
        ]
        regexp = re.compile("|".join(regexps), re.IGNORECASE)
        if not regexp.search(self.path):
            raise ValueError(f"Resource '{self.path}' is not supported.")


@dataclass(frozen=True)
class ApiRequestArguments(Argument):
    endpoint: Endpoint
    version: str = settings.VERSION
    content_negotiation: str = "application/json"
    verbosity: str = settings.VERBOSITY
    method: str = "GET"

    def __post_init__(self):

        # verbosity levels
        if self.verbosity.lower() not in settings.VERBOSITY_lEVELS:
            raise ValueError(
                f"'{self.verbosity}' is not a valid verbosity level. Please consider one of: "
                f"'{', '.join(settings.VERBOSITY_lEVELS)}'"
            )

        # methods
        if self.method.lower() not in settings.ALLOWED_METHODS:
            raise ValueError(
                f"'{self.method}' is not a valid choice. Please consider one of: "
                f"'{', '.join(settings.ALLOWED_METHODS)}'"
            )

        # content negotiation
        if self.content_negotiation not in settings.CONTENT_NEGOTIATIONS:
            raise ValueError(
                f"'{self.content_negotiation}' is not a valid content negotiation. "
                f"Please consider one of: '{', '.join(settings.CONTENT_NEGOTIATIONS)}'"
            )

        # version
        if self.version not in settings.VERSIONS:
            raise ValueError(
                f"'{self.version}' is not a valid version. Please consider one of: "
                f"'{''.join(settings.VERSIONS)}'"
            )


@dataclass
class ResourceUri(Argument):
    endpoint: str = field(init=False)
    resource_name: str
    resource_id: Optional[Union[str, int]]
    sub_resource_name: Optional[str]
    sub_resource_id: Optional[Union[str, int]]

    def __post_init__(self):

        # build uri
        uri = f"/{self.resource_name}"
        if self.resource_id:
            uri += f"/{self.resource_id}"
            if self.sub_resource_name:
                uri += f"/{self.sub_resource_name}"
                if self.sub_resource_id:
                    uri += f"/{self.sub_resource_id}"
        self.endpoint = uri


@dataclass(frozen=True)
class ResourceVerbosity(Argument):
    verbosity: str = settings.VERBOSITY
    iterate: bool = False

    def __post_init__(self):
        # if we want to iterate we need metadata, verbosity higher or equal than normal
        if (
            self.iterate
            and self.verbosity.lower() not in settings.ITERATE_VERBOSITY_lEVELS
        ):
            raise ValueError(
                f"'{self.verbosity}' is not a valid verbosity level. Please consider one of: "
                f"'{', '.join(settings.ITERATE_VERBOSITY_lEVELS)}'"
            )
