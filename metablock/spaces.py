from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from typing_extensions import Annotated, Doc

from .components import Callback, Manager
from .schema import (
    Block,
    Certificate,
    Deployment,
    Space,
    SpaceExtension,
    SpaceNameServers,
)
from .utils import Filter, compact_dict, filter_as_tuple


@dataclass
class Spaces(Manager):
    """Manage spaces and the blocks and extensions inside them"""

    path: ClassVar[str] = "spaces"

    async def get_list(self, **kwargs: Any) -> list[Space]:
        """Get the list of spaces in the organization"""
        data = await self.cli.get(self.url, **kwargs)
        return [Space(**s) for s in data]

    async def create(self, **data: Any) -> Space:
        """Create a new space in the organization"""
        payload = await self.cli.post(self.url, json=data)
        return Space(**payload)

    async def get(self, space_id_or_name: str) -> Space:
        """Get a space by id or name"""
        data = await self.cli.get(f"{self.url}/{space_id_or_name}")
        return Space(**data)

    async def update(self, space_id_or_name: str, **kwargs: Any) -> Space:
        """Update a space by id or name"""
        data = await self.cli.patch(f"{self.url}/{space_id_or_name}", json=kwargs)
        return Space(**data)

    async def nameservers(self, space_id_or_name: str) -> SpaceNameServers:
        """Get the nameservers to configure at the domain registrar"""
        data = await self.cli.get(f"{self.url}/{space_id_or_name}/nameservers")
        return SpaceNameServers(**data)

    async def blocks(
        self,
        space_id_or_name: str,
        *,
        name: Annotated[Filter[str] | None, Doc("Filter by block name")] = None,
        html: Annotated[bool | None, Doc("Filter by HTML blocks")] = None,
        **kwargs: Any,
    ) -> list[Block]:
        """Get a list of blocks in the space"""
        data = await self.cli.get(
            f"{self.url}/{space_id_or_name}/blocks",
            params=compact_dict(name=filter_as_tuple(name), html=html),
            **kwargs,
        )
        return [Block(**d) for d in data]

    async def create_block(
        self, space_id_or_name: str, name: str, **kwargs: Any
    ) -> Block:
        """Create a new block in the space"""
        data = await self.cli.post(
            f"{self.url}/{space_id_or_name}/blocks",
            json=dict(name=name, **kwargs),
        )
        return Block(**data)

    async def extensions(self, space_id_or_name: str) -> list[SpaceExtension]:
        """Get a list of extensions in the space"""
        data = await self.cli.get(f"{self.url}/{space_id_or_name}/extensions")
        return [SpaceExtension(**e) for e in data]

    async def add_extension(
        self, space_id_or_name: str, name: str, config: dict | None = None
    ) -> SpaceExtension:
        """Add/update an extension in a space"""
        data = await self.cli.put(
            f"{self.url}/{space_id_or_name}/extensions",
            json=dict(name=name, config=config or {}),
        )
        return SpaceExtension(**data)


@dataclass
class Blocks(Manager):
    """Manage blocks, their routes and their deployments"""

    path: ClassVar[str] = "blocks"

    async def get(self, block_id: str) -> Block:
        """Get a block by id"""
        data = await self.cli.get(f"{self.url}/{block_id}")
        return Block(**data)

    async def update(self, block_id: str, **kwargs: Any) -> Block:
        """Update a block by id"""
        data = await self.cli.patch(f"{self.url}/{block_id}", json=kwargs)
        return Block(**data)

    async def delete(self, block_id: str) -> None:
        """Delete a block by id"""
        await self.cli.delete(f"{self.url}/{block_id}")

    async def certificate(self, block_id: str) -> Certificate:
        """Get the TLS certificate of a block"""
        data = await self.cli.get(f"{self.url}/{block_id}/certificate")
        return Certificate(**data)

    async def deployments(
        self,
        block_id: str,
        *,
        env: Annotated[str | None, Doc("Filter by deployment environment")] = None,
        limit: Annotated[int | None, Doc("Maximum number of deployments")] = None,
        cursor: Annotated[str | None, Doc("Cursor for pagination")] = None,
    ) -> list[Deployment]:
        """Get a list of deployments for the block"""
        data = await self.cli.get(
            f"{self.url}/{block_id}/deployments",
            params=compact_dict(env=env, limit=limit, cursor=cursor),
        )
        return [Deployment(**d) for d in data]

    async def ship(
        self,
        block_id: str,
        bundle_path: str | Path,
        name: str = "",
        env: str = "stage",
        **kwargs: Any,
    ) -> dict:
        """Deploy a bundle to the block"""
        p = Path(bundle_path)
        return await self.cli.post(
            f"{self.url}/{block_id}/deployments",
            data=dict(name=name, env=env),
            files=dict(bundle=(p.name, p.read_bytes())),
            **kwargs,
        )

    async def add_route(
        self, block_id: str, *, callback: Callback | None = None, **kwargs: Any
    ) -> dict:
        """Add a new route to the block"""
        return await self.cli.post(
            f"{self.url}/{block_id}/routes", json=kwargs, callback=callback
        )

    async def update_route(
        self,
        block_id: str,
        name: str,
        *,
        callback: Callback | None = None,
        **kwargs: Any,
    ) -> dict:
        """Update a route in the block"""
        return await self.cli.patch(
            f"{self.url}/{block_id}/routes/{name}", json=kwargs, callback=callback
        )
