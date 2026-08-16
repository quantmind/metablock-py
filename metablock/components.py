from __future__ import annotations

import json
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Awaitable, Callable, ClassVar

from httpx2 import Response as ClientResponse

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


@dataclass
class Manager:
    """Base class for API resource managers.

    A manager owns a path below the API root and issues requests through the
    client. Managers hold the behaviour; the models in `metablock.schema` are
    plain data generated from the OpenAPI spec and carry no client reference.
    """

    cli: Metablock
    path: ClassVar[str] = ""

    @property
    def url(self) -> str:
        return f"{self.cli.url}/{self.path}"
