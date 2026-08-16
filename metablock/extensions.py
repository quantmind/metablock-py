from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from typing_extensions import Annotated, Doc

from .components import Manager
from .schema import Extension
from .utils import compact_dict


@dataclass
class Extensions(Manager):
    """Manage the publicly available extensions"""

    path: ClassVar[str] = "extensions"

    async def get_list(self, *, cursor: str | None = None) -> list[Extension]:
        """Get a list of extensions"""
        data = await self.cli.get(self.url, params=compact_dict(cursor=cursor))
        return [Extension(**e) for e in data]


@dataclass
class OrgExtensions(Manager):
    """Manage the extensions owned by the organization"""

    path: ClassVar[str] = "orgs-extensions"

    async def get_list(
        self,
        *,
        name: Annotated[str | None, Doc("Filter by extension name")] = None,
        search: Annotated[str | None, Doc("Search extensions")] = None,
        limit: Annotated[int | None, Doc("Maximum number of extensions")] = None,
        cursor: Annotated[str | None, Doc("Cursor for pagination")] = None,
        **kwargs: Any,
    ) -> list[Extension]:
        """Get a list of extensions owned by the organization"""
        data = await self.cli.get(
            self.url,
            params=compact_dict(name=name, search=search, limit=limit, cursor=cursor),
            **kwargs,
        )
        return [Extension(**e) for e in data]

    async def create(self, **data: Any) -> Extension:
        """Create a new extension in the organization"""
        payload = await self.cli.post(self.url, json=data)
        return Extension(**payload)
