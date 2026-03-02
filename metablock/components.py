from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Protocol, runtime_checkable

from httpx import Response as ClientResponse
from pydantic import BaseModel, ConfigDict, Field

from .utils import as_dict

if TYPE_CHECKING:  # pragma: no cover
    from .client import Metablock


Callback = Callable[[ClientResponse], Awaitable[Any]]


class MetablockError(Exception):
    pass


class MetablockResponseError(MetablockError):
    def __init__(self, response: ClientResponse, message: Any = "") -> None:
        self.response = response
        self.message = as_dict(message, "message")
        self.message["request_url"] = str(response.url)
        self.message["request_method"] = response.request.method
        self.message["response_status"] = response.status_code

    @property
    def status(self) -> int:
        return self.response.status_code

    def __str__(self) -> str:
        return json.dumps(self.message, indent=4)


@runtime_checkable
class HttpComponent(Protocol):
    @property
    def cli(self) -> Metablock:  # pragma: no cover
        ...

    @property
    def url(self) -> str:  # pragma: no cover
        ...


class MetablockComponent(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    root: HttpComponent = Field(exclude=True)
    root_path: str = Field(exclude=True)

    @property
    def cli(self) -> Metablock:
        return self.root.cli

    @property
    def url(self) -> str:
        return f"{self.root.url}/{self.root_path}"


class MetablockEntity(MetablockComponent):
    """A Metablock entity"""

    id: str = Field(description="The unique identifier of the entity")
