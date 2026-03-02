from __future__ import annotations

from typing import Any

from pydantic import Field

from .components import MetablockComponent, MetablockEntity
from .extensions import Extension, Extensions
from .spaces import Space


class OrgSpaces(MetablockComponent):
    async def get_list(self) -> list[Space]:
        data = await self.cli.get(self.url)
        return [
            Space(root=self.cli, root_path=f"spaces/{s['name']}", **s) for s in data
        ]

    async def create(self, **data: Any) -> Space:
        data = await self.cli.post(f"{self.url}", json=data)
        return Space(root=self.cli, root_path=f"spaces/{data['name']}", **data)


class OrgExtensions(Extensions):
    async def create(self, **data: Any) -> Extension:
        data = await self.cli.post(f"{self.url}", json=data)
        return Extension(**data)


class Org(MetablockEntity):
    """Object representing an Organization"""

    full_name: str = Field(description="The name of the organization")
    short_name: str = Field(description="The short name of the organization")
    country: str = Field(default="", description="The country of the organization")
    email: str = Field(description="The email of the organization")
    additional_info: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional information about the organization",
    )

    @property
    def spaces(self) -> OrgSpaces:
        return OrgSpaces(root=self, root_path="spaces")

    @property
    def extensions(self) -> OrgExtensions:
        return OrgExtensions(root=self, root_path="extensions")

    @property
    def members(self) -> Members:
        return Members(root=self, root_path="members")

    @property
    def roles(self) -> Roles:
        return Roles(root=self, root_path="roles")

    async def add_info(self, **data: Any) -> dict:
        return await self.cli.patch(f"{self.url}/info", json=data)


class Member(MetablockEntity):
    """Object representing a organization member"""


class Role(MetablockEntity):
    """Object representing a organization role"""


class Members(MetablockComponent):
    """Metablock organization members"""


class Roles(MetablockComponent):
    """Metablock organizations"""


class Orgs(MetablockComponent):
    """Metablock organizations"""

    async def get(self, name_or_id: str) -> Org:
        """Get an organization by name or id"""
        data = await self.cli.get(f"{self.url}/{name_or_id}")
        return Org(root=self, root_path=data["short_name"], **data)
