import re

from typing import Optional, Union
from pydantic import BaseModel, ValidationError, validator, root_validator
from mopinion_api import settings


__all__ = [
    "Credentials",
    "EndPoint",
    "ApiRequestArguments",
    "ResourceUri",
    "ResourceVerbosity",
]


class Credentials(BaseModel):
    public_key: str
    private_key: str


class EndPoint(BaseModel):
    path: str

    @validator("path")
    def validate_path(cls, v):
        # endpoint must start with '/'
        if not v.startswith("/"):
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
        if not regexp.search(v):
            raise ValueError(f"Resource '{v}' is not supported.")

        return v


class ApiRequestArguments(BaseModel):
    endpoint: EndPoint
    version: str = settings.VERSION
    content_negotiation: str = "application/json"
    verbosity: str = settings.VERBOSITY
    method: str = "GET"

    @validator("verbosity")
    def validate_verbosity(cls, v):
        # verbosity levels
        if v.lower() not in settings.VERBOSITY_lEVELS:
            raise ValueError(
                f"'{v}' is not a valid verbosity level. Please consider one of: "
                f"'{', '.join(settings.VERBOSITY_lEVELS)}'"
            )
        return v

    @validator("method")
    def validate_mehtod(cls, v):
        if v.lower() not in settings.ALLOWED_METHODS:
            raise ValueError(
                f"'{v}' is not a valid choice. Please consider one of: "
                f"'{', '.join(settings.ALLOWED_METHODS)}'"
            )
        return v

    @validator("content_negotiation")
    def validate_content_negotiation(cls, v):
        if v not in settings.CONTENT_NEGOTIATIONS:
            raise ValueError(
                f"'{v}' is not a valid content negotiation. "
                f"Please consider one of: '{', '.join(settings.CONTENT_NEGOTIATIONS)}'"
            )
        return v

    @validator("version")
    def validate_version(cls, v):
        if v not in settings.VERSIONS:
            raise ValueError(
                f"'{v}' is not a valid version. Please consider one of: "
                f"'{''.join(settings.VERSIONS)}'"
            )
        return v


class ResourceUri(BaseModel):
    endpoint: str = None
    resource_name: str
    resource_id: Optional[Union[str, int]]
    sub_resource_name: Optional[str]
    sub_resource_id: Optional[Union[str, int]]

    @root_validator
    def validate_endpoint(cls, values):
        v = f"/{values['resource_name']}"
        if values.get("resource_id"):
            v += f"/{values['resource_id']}"
            if values.get("sub_resource_name"):
                v += f"/{values['sub_resource_name']}"
                if values.get("sub_resource_id"):
                    v += f"/{values['sub_resource_id']}"
        values["endpoint"] = v
        return values


class ResourceVerbosity(BaseModel):
    verbosity: str = settings.VERBOSITY
    iterate: bool = False

    @root_validator
    def validate_verbosity(cls, values):
        # if we want to iterate we need metadata, verbosity higher or equal than normal
        if (
            values["iterate"]
            and values["verbosity"].lower() not in settings.ITERATE_VERBOSITY_lEVELS
        ):
            raise ValueError(
                f"'{values['verbosity']}' is not a valid verbosity level. Please "
                f"consider one of: '{', '.join(settings.ITERATE_VERBOSITY_lEVELS)}'"
            )
        return values
