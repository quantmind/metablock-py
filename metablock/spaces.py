from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from .components import MetablockComponent, MetablockEntity


# Space
class Space(MetablockEntity):
    """Object representing a space"""

    name: str = Field(description="The name of the space")
    domain: str = Field(description="The domain of the space")
    org_id: str = Field(description="The organization id of the space")
    org_name: str = Field(description="The organization name of the space")

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
        return Space(root=self.cli, root_path=data["id"], **data)


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
    # space: Space = Field(description="The space of the block")

    @property
    def deployments(self) -> Deployments:
        return Deployments(root=self, root_path="deployments")

    async def config(self, *, callback: Any = None) -> dict:
        return await self.cli.get(f"{self.url}/config", callback=callback)

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
        return Block(
            root=self.cli,
            root_path=data["id"],
            is_root=data.pop("root", False),
            **data,
        )

    async def patch(self, block_id: str, **kwargs: Any) -> Block:
        """Update a block by id"""
        data = await self.cli.patch(f"{self.url}/{block_id}", json=kwargs)
        return Block(
            root=self.cli,
            root_path=data["id"],
            is_root=data.pop("root", False),
            **data,
        )


class SpaceBlocks(Blocks):
    async def get_list(self) -> list[Block]:
        """Get a list of blocks in the space"""
        data = await self.cli.get(self.url)
        return [
            Block(root=self.cli, root_path=s["id"], is_root=s.pop("root", False), **s)
            for s in data
        ]

    async def create(self, name: str, **kwargs: Any) -> Block:
        """Create a new block in the space"""
        data = await self.cli.post(self.url, json=dict(name=name, **kwargs))
        return Block(
            root=self.cli,
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


class Deployment(MetablockEntity):
    """Object representing a deployment"""


class Deployments(MetablockComponent):
    """deployments"""


# Domain


class Domains(MetablockComponent):
    async def check(self, domain: str) -> str:
        return await self.cli.get(f"{self.url}/check/{domain}")
