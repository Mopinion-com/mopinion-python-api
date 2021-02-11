from dataclasses import dataclass
from dataclasses import field
from mopinion import settings
from typing import Optional
from typing import Union

import re


__all__ = [
    "Credentials",
    "EndPoint",
    "ApiRequestArguments",
    "ResourceUri",
    "ResourceVerbosity",
]


class Argument:
    pass


@dataclass(frozen=True)
class Credentials(Argument):
    public_key: str
    private_key: str


@dataclass(frozen=True)
class EndPoint(Argument):
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
            r"/datasets/\d+$",
            r"/datasets/\d+/fields$",
            r"/reports/\d+/fields$",
            r"/datasets/\d+/feedback$",
            r"/reports/\d+/feedback$",
            r"/reports/\d+$",
            r"/reports$",
        ]
        regexp = re.compile("|".join(regexps), re.IGNORECASE)
        if not regexp.search(self.path):
            raise ValueError(f"Resource '{self.path}' is not supported.")


@dataclass(frozen=True)
class ApiRequestArguments(Argument):
    endpoint: EndPoint
    content_negotiation: str
    verbosity: str
    version: str = None

    def __post_init__(self):
        # verbosity levels
        if self.verbosity.lower() not in settings.VERBOSITY_lEVELS:
            raise ValueError(
                f"'{self.verbosity}' is not a valid verbosity level. Please consider one of: "
                f"'{', '.join(settings.VERBOSITY_lEVELS)}'"
            )

        if self.content_negotiation not in settings.CONTENT_NEGOTIATIONS:
            raise ValueError(
                f"'{self.content_negotiation}' is not a valid content negotiation. "
                f"Please consider one of: '{', '.join(settings.CONTENT_NEGOTIATIONS)}'"
            )

        if self.version and self.version not in settings.VERSIONS:
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

    def __post_init__(self):
        from mopinion.client import MopinionClient

        allowed_resources = [
            MopinionClient.RESOURCE_ACCOUNT,
            MopinionClient.RESOURCE_DEPLOYMENTS,
            MopinionClient.RESOURCE_DATASETS,
            MopinionClient.RESOURCE_REPORTS,
        ]
        allowed_subresources = [
            MopinionClient.SUBRESOURCE_FEEDBACK,
            MopinionClient.SUBRESOURCE_FIELDS,
        ]

        if self.resource_name and self.resource_name not in allowed_resources:
            raise ValueError(
                f"Resource name {self.resource_name} must be one of {allowed_resources}"
            )

        if (
            self.sub_resource_name
            and self.sub_resource_name not in allowed_subresources
        ):
            raise ValueError(
                f"Subresource name {self.sub_resource_name} must be one of {allowed_subresources}"
            )

        endpoint = f"/{self.resource_name}"
        if self.resource_id:
            endpoint += f"/{self.resource_id}"
            if self.sub_resource_name:
                endpoint += f"/{self.sub_resource_name}"
        self.endpoint = endpoint


@dataclass(frozen=True)
class ResourceVerbosity(Argument):
    verbosity: str
    iterator: bool

    def __post_init__(self):
        # if we want to iterate we need metadata, verbosity higher or equal than normal
        if (
            self.iterator
            and self.verbosity.lower() not in settings.ITERATE_VERBOSITY_lEVELS
        ):
            raise ValueError(
                f"'{self.verbosity}' is not a valid verbosity level. Please "
                f"consider one of: '{', '.join(settings.ITERATE_VERBOSITY_lEVELS)}'"
            )
