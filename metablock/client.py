from __future__ import annotations

import logging
import os
import sys
from dataclasses import dataclass, field
from typing import Any, Self

from httpx2 import AsyncClient
from httpx2 import Response as ClientResponse

from .components import Callback, MetablockResponseError
from .extensions import Extensions, OrgExtensions
from .orgs import Orgs
from .spaces import Blocks, Spaces
from .user import Users

DEFAULT_USER_AGENT = f"Python/{'.'.join(map(str, sys.version_info[:2]))} metablock"

logger = logging.getLogger("metablock.client")


@dataclass
class Metablock:
    """Metablock client

    Entry point to the API. Resource managers hang off the client and return the
    plain data models in `metablock.schema`.
    """

    url: str = field(
        default_factory=lambda: os.environ.get(
            "METABLOCK_URL", "https://api.metablock.io/v1"
        )
    )
    auth_key: str = field(default_factory=lambda: os.getenv("METABLOCK_API_TOKEN", ""))
    org_id: str = field(default_factory=lambda: os.getenv("METABLOCK_ORG_ID", ""))
    auth_key_name: str = "x-metablock-api-key"
    org_id_name: str = "x-metablock-org-id"
    session: AsyncClient | None = None
    user_agent: str = DEFAULT_USER_AGENT
    session_owner: bool = field(init=False, default=False)

    def __post_init__(self) -> None:
        self.session_owner = self.session is None

    @property
    def orgs(self) -> Orgs:
        return Orgs(self)

    @property
    def spaces(self) -> Spaces:
        return Spaces(self)

    @property
    def blocks(self) -> Blocks:
        return Blocks(self)

    @property
    def extensions(self) -> Extensions:
        return Extensions(self)

    @property
    def org_extensions(self) -> OrgExtensions:
        return OrgExtensions(self)

    @property
    def user(self) -> Users:
        return Users(self)

    async def close(self) -> None:
        if self.session and self.session_owner:
            await self.session.aclose()
            self.session = None

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: type, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    async def spec(self) -> dict:
        """Get the OpenAPI specification of the API"""
        return await self.request(f"{self.url}/openapi.json")

    async def get(self, url: str, **kwargs: Any) -> Any:
        """Make a GET request to the API"""
        kwargs["method"] = "GET"
        return await self.request(url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> Any:
        """Make a PATCH request to the API"""
        kwargs["method"] = "PATCH"
        return await self.request(url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> Any:
        """Make a POST request to the API"""
        kwargs["method"] = "POST"
        return await self.request(url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> Any:
        """Make a PUT request to the API"""
        kwargs["method"] = "PUT"
        return await self.request(url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> Any:
        """Make a DELETE request to the API"""
        kwargs["method"] = "DELETE"
        return await self.request(url, **kwargs)

    async def request(
        self,
        url: str,
        method: str = "",
        headers: dict[str, str] | None = None,
        callback: Callback | bool | None = None,
        wrap: Any = None,
        **kw: Any,
    ) -> Any:
        """Make a request to the API with the given method, url, headers and body."""
        if not self.session:
            self.session = AsyncClient()
        method = method or "GET"
        headers_ = self.get_default_headers()
        headers_.update(headers or ())
        response = await self.session.request(method, url, headers=headers_, **kw)
        if callback is True:
            return response
        elif callback:
            return await callback(response)
        else:
            return await self.handle_response(response, wrap=wrap)

    async def handle_response(self, response: ClientResponse, wrap: Any = None) -> Any:
        if response.status_code == 204:
            return True
        if response.status_code >= 400:
            try:
                data = response.json()
            except Exception:
                data = response.text
            raise MetablockResponseError(response, data)
        response.raise_for_status()
        data = response.json()
        return wrap(data) if wrap else data

    def get_default_headers(self) -> dict[str, str]:
        headers = {
            "user-agent": self.user_agent,
            "accept": "application/json",
        }
        if self.auth_key:
            headers[self.auth_key_name] = self.auth_key
        if self.org_id:
            headers[self.org_id_name] = self.org_id
        return headers
