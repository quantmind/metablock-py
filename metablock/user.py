from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Self

from pydantic import BaseModel, Field

from .components import MetablockEntity, MetablockResponseError
from .orgs import Org

if TYPE_CHECKING:  # pragma: no cover
    from .client import Metablock


class OrgMember(BaseModel):
    """Object representing an Organization"""

    org: Org = Field(description="Organization")
    roles: list[str] = Field(description="The user's roles in the organization")

    @classmethod
    def from_cli(cls, cli: Metablock, **data: Any) -> Self:
        name = data["org_name"]
        org = Org(
            root=cli,
            root_path=f"orgs/{name}",
            id=data["org_id"],
            email=data["org_email"],
            short_name=name,
            full_name=data["org_full_name"],
        )
        return cls(org=org, roles=data["roles"])


class User(MetablockEntity):
    """Object representing a Metablock user"""

    first_name: str = Field(description="The user's first name")
    last_name: str = Field(description="The user's last name")
    email: str = Field(description="The user's email address")
    mobile_phone: str | None = Field(
        default=None,
        description="The user's mobile phone number",
    )
    created: datetime = Field(description="The user's account creation date")
    status: str = Field(description="The user's account status")

    async def orgs(self, **kwargs: Any) -> list[OrgMember]:
        """List user organizations"""
        orgs = await self.cli.get(f"{self.url}/orgs", **kwargs)
        return [OrgMember.from_cli(self.cli, **data) for data in orgs]

    async def get_permissions(self, **kwargs: Any) -> list[dict]:
        """List user permissions"""
        return await self.cli.get(f"{self.url}/permissions", **kwargs)

    async def tokens(self, **kwargs: Any) -> list[dict]:
        return await self.cli.get(f"{self.url}/tokens", **kwargs)

    async def create_token(self, **kwargs: Any) -> dict:
        return await self.cli.post(f"{self.url}/tokens", **kwargs)

    async def delete_token(self, token_id: str, **kwargs: Any) -> dict:
        return await self.cli.delete(f"{self.url}/tokens/{token_id}", **kwargs)

    async def check_password(self, password: str, **kwargs: Any) -> bool:
        try:
            return await self.cli.post(
                f"{self.url}/password", json=dict(password=password), **kwargs
            )
        except MetablockResponseError as exc:
            if exc.status == 401:
                return False
            else:
                raise
