import asyncio
import os
from pathlib import Path

import click
import jinja2
import yaml

from metablock import Metablock, __version__
from metablock.utils import temp_zipfile

METABLOCK_SPACE = os.environ.get("METABLOCK_SPACE", "")
METABLOCK_ENV = os.environ.get("METABLOCK_ENV", "prod")
METABLOCK_NAME = os.environ.get("METABLOCK_NAME", "shipped from metablock-py")
METABLOCK_BLOCK_ID = os.environ.get("METABLOCK_BLOCK_ID", "")
METABLOCK_API_TOKEN = os.environ.get("METABLOCK_API_TOKEN", "")
METABLOCK_ORG_ID = os.environ.get("METABLOCK_ORG_ID", "")
METABLOCK_API_TIMEOUT = int(os.environ.get("METABLOCK_API_TIMEOUT", "60"))


def manifest(file_path: Path, params: dict) -> str:
    env = jinja2.Environment()
    template = env.from_string(file_path.read_text())
    return template.render(**params)


@click.group()
@click.version_option(version=__version__)
def main() -> None:
    pass


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--space",
    "space_name",
    help="Space name",
    default=METABLOCK_SPACE,
    show_default=True,
)
@click.option(
    "--token",
    help="metablock API token",
    default=METABLOCK_API_TOKEN,
)
@click.option(
    "--org",
    "org_id",
    help="metablock organization id the request acts within",
    default=METABLOCK_ORG_ID,
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Do not apply changes, just show what would be done",
)
def apply(path: str, space_name: str, token: str, org_id: str, dry_run: bool) -> None:
    """Apply metablock manifest to a metablock space"""
    asyncio.run(
        _apply(
            path,
            space_name or METABLOCK_SPACE,
            token or METABLOCK_API_TOKEN,
            org_id or METABLOCK_ORG_ID,
            dry_run=dry_run,
        )
    )


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--env",
    help="Environment to ship to",
    type=click.Choice(["prod", "stage"]),
    default=METABLOCK_ENV,
    show_default=True,
)
@click.option(
    "--block-id",
    help="Block ID",
    default=METABLOCK_BLOCK_ID,
    show_default=True,
)
@click.option(
    "--name",
    help="Optional deployment name",
    default=METABLOCK_NAME,
    show_default=True,
)
@click.option(
    "--token",
    help="metablock API token",
    default=METABLOCK_API_TOKEN,
)
@click.option(
    "--org",
    "org_id",
    help="metablock organization id the request acts within",
    default=METABLOCK_ORG_ID,
)
@click.option(
    "--timeout",
    help="Timeout in seconds for the upload request",
    type=int,
    default=METABLOCK_API_TIMEOUT,
    show_default=True,
)
def ship(
    path: str,
    env: str,
    block_id: str,
    name: str,
    token: str,
    org_id: str,
    timeout: int,
) -> None:
    """Deploy a new version of an html block"""
    asyncio.run(
        _ship(
            path,
            env or METABLOCK_ENV,
            block_id or METABLOCK_BLOCK_ID,
            name or METABLOCK_NAME,
            token or METABLOCK_API_TOKEN,
            org_id or METABLOCK_ORG_ID,
            timeout or METABLOCK_API_TIMEOUT,
        )
    )


async def _apply(
    path: str, space_name: str, token: str, org_id: str, dry_run: bool
) -> None:
    if not token:
        click.echo("metablock API token is required", err=True)
        raise click.Abort()
    if not space_name:
        click.echo("metablock space is required", err=True)
        raise click.Abort()
    p = Path(path)
    blocks = []
    for file_path in p.glob("*.yaml"):
        name = file_path.name.split(".")[0]
        text = manifest(file_path, dict(space=space_name, block=name))
        if dry_run:
            click.echo(text)
        else:
            blocks.append((name, yaml.safe_load(text)))
    if not blocks:
        click.echo("nothing to do")
        raise click.Abort()
    async with Metablock(auth_key=token, org_id=org_id) as mb:
        space = await mb.spaces.get(space_name)
        space_blocks = await mb.spaces.blocks(space.id)
        click.echo(f"space {space.name} has {len(space_blocks)} blocks")
        by_name = {s.name: s for s in space_blocks}
        for name, config in blocks:
            block = by_name.get(name)
            if block:
                # update
                await mb.blocks.update(block.id, **config)
                click.echo(f"updated block {name}")
            else:
                # create
                await mb.spaces.create_block(space.id, name=name, **config)
                click.echo(f"created new block {name}")


async def _ship(
    path: str,
    env: str,
    block_id: str,
    name: str,
    token: str,
    org_id: str,
    timeout: int = METABLOCK_API_TIMEOUT,
) -> None:
    if not token:
        click.echo("metablock API token is required", err=True)
        raise click.Abort()
    if not block_id:
        click.echo("metablock block-id is required", err=True)
        raise click.Abort()
    p = Path(path)
    try:
        with temp_zipfile(p) as zip_path:
            click.echo(f"Created zip file: {zip_path}")
            async with Metablock(auth_key=token, org_id=org_id) as mb:
                block = await mb.blocks.get(block_id)
                await mb.blocks.ship(
                    block.id,
                    zip_path,
                    name=name,
                    env=env,
                    timeout=timeout,
                )
                click.echo(f"shipped {zip_path} to {block.name} {env}")
    except ValueError as e:
        click.echo(str(e), err=True)
        raise click.Abort() from None
