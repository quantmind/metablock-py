from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from .components import Manager
from .schema import Org
from .schema import OrgRoleNamedPermissionsOrgPermission as OrgRole


@dataclass
class Orgs(Manager):
    """Manage organizations and their roles"""

    path: ClassVar[str] = "orgs"

    async def get(self, org_id_or_name: str) -> Org:
        """Get an organization by name or id"""
        data = await self.cli.get(f"{self.url}/{org_id_or_name}")
        return Org(**data)

    async def create(self, **data: Any) -> Org:
        """Create a new organization"""
        payload = await self.cli.post(self.url, json=data)
        return Org(**payload)

    async def update(self, org_id_or_name: str, **data: Any) -> Org:
        """Update an organization by name or id"""
        payload = await self.cli.patch(f"{self.url}/{org_id_or_name}", json=data)
        return Org(**payload)

    async def roles(self, org_id_or_name: str) -> list[OrgRole]:
        """Get a list of roles in the organization"""
        data = await self.cli.get(f"{self.url}/{org_id_or_name}/roles")
        return [OrgRole(**r) for r in data]

    async def create_role(self, org_id_or_name: str, **data: Any) -> dict:
        """Create a new role in the organization"""
        return await self.cli.post(f"{self.url}/{org_id_or_name}/roles", json=data)

    async def get_role(self, org_id_or_name: str, role_id_or_name: str) -> OrgRole:
        """Get a role by id or name"""
        data = await self.cli.get(
            f"{self.url}/{org_id_or_name}/roles/{role_id_or_name}"
        )
        return OrgRole(**data)

    async def update_role(
        self, org_id_or_name: str, role_id_or_name: str, **data: Any
    ) -> OrgRole:
        """Update a role by id or name"""
        payload = await self.cli.patch(
            f"{self.url}/{org_id_or_name}/roles/{role_id_or_name}", json=data
        )
        return OrgRole(**payload)

    async def delete_role(self, org_id_or_name: str, role_id_or_name: str) -> None:
        """Delete a role by id or name"""
        await self.cli.delete(f"{self.url}/{org_id_or_name}/roles/{role_id_or_name}")
