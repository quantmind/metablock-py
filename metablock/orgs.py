from __future__ import annotations

from typing import Any

from .components import CrudComponent, MetablockEntity
from .extensions import Extension, Extensions, Plugin, Plugins
from .spaces import Space, Spaces


class OrgSpaces(Spaces):
    def list_create_url(self) -> str:
        return "%s/%s" % (self.root.url, self.name)


class OrgExtensions(Extensions):
    def list_create_url(self) -> str:
        return "%s/%s" % (self.root.url, self.name)


class OrgPlugins(Plugins):
    def list_create_url(self) -> str:
        return "%s/%s" % (self.root.url, self.name)


class Org(MetablockEntity):
    """Object representing an Organization"""

    @property
    def name(self) -> str:
        return self.data.get("short_name", "")

    @property
    def spaces(self) -> OrgSpaces:
        return OrgSpaces(self, Space, "spaces")

    @property
    def plugins(self) -> OrgPlugins:
        return OrgPlugins(self, Plugin, "plugins")

    @property
    def extensions(self) -> OrgExtensions:
        return OrgExtensions(self, Extension, "extensions")

    @property
    def members(self) -> Members:
        return Members(self, Member)

    @property
    def roles(self) -> Roles:
        return Roles(self, Role)

    async def add_info(self, **data: Any) -> dict:
        return await self.cli.patch(f"{self.url}/info", json=data)


class Member(MetablockEntity):
    """Object representing a organization member"""


class Role(MetablockEntity):
    """Object representing a organization role"""


class Members(CrudComponent[Member]):
    """Metablock organization members"""

    @property
    def url(self) -> str:
        return f"{self.root.url}/{self.name}"


class Roles(CrudComponent):
    """Metablock organizations"""

    Entity = Role

    @property
    def url(self) -> str:
        return f"{self.root.url}/{self.name}"


class Orgs(CrudComponent[Org]):
    """Metablock organizations"""
