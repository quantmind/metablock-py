from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, Field
from typing_extensions import Annotated, Doc

from .components import MetablockComponent, MetablockEntity
from .utils import Filter, compact_dict, filter_as_tuple

if TYPE_CHECKING:
    from .client import Metablock


# Space
class Space(MetablockEntity):
    """Object representing a space"""

    name: str = Field(description="The name of the space")
    domain: str = Field(description="The domain of the space")
    org_id: str = Field(description="The organization id of the space")
    org_name: str = Field(description="The organization name of the space")
    hosted: bool = Field(
        description="Whether the space is hosted in metablock or self-hosted",
    )

    @property
    def blocks(self) -> SpaceBlocks:
        return SpaceBlocks(root=self, root_path="blocks")

    @property
    def extensions(self) -> SpaceExtensions:
        return SpaceExtensions(root=self, root_path="extensions")


class Spaces(MetablockComponent):
    """Spaces"""

    async def get(self, space_id_or_name: str) -> Space:
        data = await self.cli.get(f"{self.url}/{space_id_or_name}")
        return Space(root=self, root_path=data["id"], **data)

    async def update(self, space_id_or_name: str, **kwargs: Any) -> Space:
        data = await self.cli.patch(f"{self.url}/{space_id_or_name}", json=kwargs)
        return Space(root=self, root_path=data["id"], **data)


class Route(BaseModel):
    id: str = Field(description="The unique identifier of the route")
    name: str = Field(description="The name of the route")
    paths: list[str] = Field(description="The paths of the route")
    methods: list[str] = Field(description="The methods of the route")
    hosts: list[str] = Field(description="The hosts of the route")
    protocols: list[str] = Field(description="The protocols of the route")
    tags: list[str] = Field(description="The tags of the route")
    strip_path: bool = Field(description="Whether to strip the path of the route")
    preserve_host: bool = Field(description="Whether to preserve the host of the route")
    https_redirect_status_code: int | None = Field(
        default=None,
        description="The status code to use for HTTPS redirection",
    )


class Certificate(BaseModel):
    serial_number: int
    version: str
    issued_on: datetime
    expires_on: datetime
    issuer: dict
    created: datetime = Field(description="The creation date of the certificate")
    cert: str = Field(description="The public certificate")
    tags: list[str] = Field(
        description="An optional set of strings",
        default_factory=list,
    )


class Block(MetablockEntity):
    name: str = Field(description="The name of the block")
    full_name: str = Field(description="The full name of the block")
    service_id: str = Field(description="The service id of the block")
    html: bool = Field(description="Whether the block is an HTML block")
    is_root: bool = Field(description="Whether the block is a root block")
    domain: str = Field(description="The domain of the block")
    routes: list[Route] = Field(
        default_factory=list,
        description="The routes of the block",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="An optional set of strings",
    )
    space: Space = Field(description="The space of the block")

    @property
    def deployments(self) -> Deployments:
        return Deployments(root=self, root_path="deployments")

    async def certificate(self) -> Certificate:
        data = await self.cli.get(f"{self.url}/certificate")
        return Certificate(**data)

    async def ship(
        self,
        bundle_path: str | Path,
        name: str = "",
        env: str = "stage",
        **kwargs: Any,
    ) -> dict:
        p = Path(bundle_path)
        return await self.cli.post(
            f"{self.url}/deployments",
            data=dict(name=name, env=env),
            files=dict(bundle=(p.name, p.read_bytes())),
            **kwargs,
        )

    async def add_route(self, *, callback: Any = None, **kwargs: Any) -> dict:
        """Add a new route to the block"""
        return await self.cli.post(f"{self.url}/routes", json=kwargs, callback=callback)

    async def update_route(
        self, name: str, *, callback: Any = None, **kwargs: Any
    ) -> dict:
        """Update a route in the block"""
        return await self.cli.patch(
            f"{self.url}/routes/{name}", json=kwargs, callback=callback
        )


class Blocks(MetablockComponent):
    """Blocks"""

    async def get(self, block_id: str) -> Block:
        """Get a block by id"""
        data = await self.cli.get(f"{self.url}/{block_id}")
        return block_from_data(self.cli, data)

    async def update(self, block_id: str, **kwargs: Any) -> Block:
        """Update a block by id"""
        data = await self.cli.patch(f"{self.url}/{block_id}", json=kwargs)
        return block_from_data(self.cli, data)

    async def delete(self, block_id: str) -> None:
        """Delete a block by id"""
        await self.cli.delete(f"{self.url}/{block_id}")


class SpaceBlocks(MetablockComponent):
    async def get_list(
        self,
        *,
        name: Annotated[Filter[str] | None, Doc("Filter by block name")] = None,
        html: Annotated[bool | None, Doc("Filter by HTML blocks")] = None,
    ) -> list[Block]:
        """Get a list of blocks in the space"""
        data = await self.cli.get(
            self.url,
            params=compact_dict(name=filter_as_tuple(name), html=html),
        )
        return [block_from_data(self.cli, d) for d in data]

    async def create(self, name: str, **kwargs: Any) -> Block:
        """Create a new block in the space"""
        data = await self.cli.post(self.url, json=dict(name=name, **kwargs))
        return block_from_data(self.cli, data)

    async def get(self, block_id_or_name: str) -> Block:
        """Get a block by id or name"""
        return await self.cli.blocks.get(block_id_or_name)

    async def update(self, block_id_or_name: str, **kwargs: Any) -> Block:
        """Update a block by id or name"""
        return await self.cli.blocks.update(block_id_or_name, **kwargs)

    async def delete(self, block_id_or_name: str) -> None:
        """Delete a block by id or name"""
        await self.cli.blocks.delete(block_id_or_name)


def block_from_data(cli: Metablock, data: dict) -> Block:
    data = data.copy()
    data["space"] = Space(
        root=cli.spaces,
        root_path=data["space"]["id"],
        **data["space"],
    )
    return Block(
        root=cli.blocks,
        root_path=data["id"],
        is_root=data.pop("root", False),
        **data,
    )


# SpaceExtension
class SpaceExtension(BaseModel):
    """Object representing an SpaceExtension"""

    id: str = Field(description="The unique identifier of the space extension")
    name: str = Field(description="The name of the extension")
    config: dict = Field(description="The configuration of the extension")
    extension_id: str = Field(description="The id of the extension")
    space_id: str = Field(description="The id of the space")
    space_name: str = Field(description="The name of the space")


class SpaceExtensions(MetablockComponent):
    async def put(self, name: str, config: dict | None = None) -> SpaceExtension:
        """Add/update an extension in a space"""
        data = await self.cli.put(self.url, json=dict(name=name, config=config or {}))
        return SpaceExtension(**data)

    async def get_list(self) -> list[SpaceExtension]:
        """Get a list of extensions in the space"""
        data = await self.cli.get(self.url)
        return [SpaceExtension(**e) for e in data]


# Deployment


class Deployment(BaseModel):
    """Object representing a deployment"""

    id: str = Field(description="The unique identifier of the deployment")
    block_id: str = Field(description="The id of the block")
    name: str = Field(description="The name of the deployment")
    env: str = Field(description="The environment of the deployment")
    created: datetime = Field(description="The creation date of the deployment")
    url: str = Field(description="The URL of the deployment")


class Deployments(MetablockComponent):
    """Block deployments"""

    async def get_list(
        self,
        *,
        env: Annotated[str | None, Doc("Filter by deployment environment")] = None,
        limit: Annotated[int | None, Doc("Maximum number of spaces to return")] = None,
        cursor: Annotated[str | None, Doc("Cursor for pagination")] = None,
    ) -> list[Deployment]:
        """Get a list of deployments for the block"""
        data = await self.cli.get(
            self.url,
            params=compact_dict(env=env, limit=limit, cursor=cursor),
        )
        return [Deployment(**d) for d in data]


# Domain


class Domains(MetablockComponent):
    async def check(self, domain: str) -> str:
        return await self.cli.get(f"{self.url}/check/{domain}")
