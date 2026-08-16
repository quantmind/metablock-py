from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from .components import Manager
from .schema import ApiToken, OrgMember, User


@dataclass
class Users(Manager):
    """Manage the authenticated user and its API tokens"""

    path: ClassVar[str] = "user"

    async def get(self, **kwargs: Any) -> User:
        """Get the user associated with the API token"""
        data = await self.cli.get(self.url, **kwargs)
        return User(**data)

    async def update(self, **data: Any) -> User:
        """Update the authenticated user"""
        payload = await self.cli.patch(self.url, json=data)
        return User(**payload)

    async def delete(self) -> None:
        """Delete the authenticated user"""
        await self.cli.delete(self.url)

    async def orgs(self, **kwargs: Any) -> list[OrgMember]:
        """List the organizations the user belongs to"""
        data = await self.cli.get(f"{self.url}/orgs", **kwargs)
        return [OrgMember(**o) for o in data]

    async def tokens(self, **kwargs: Any) -> list[ApiToken]:
        """List the user API tokens"""
        data = await self.cli.get(f"{self.url}/tokens", **kwargs)
        return [ApiToken(**t) for t in data]

    async def create_token(self, **data: Any) -> ApiToken:
        """Create a new API token for the user"""
        payload = await self.cli.post(f"{self.url}/tokens", json=data)
        return ApiToken(**payload)

    async def delete_token(self, token_id: str) -> None:
        """Delete one of the user API tokens"""
        await self.cli.delete(f"{self.url}/tokens/{token_id}")
