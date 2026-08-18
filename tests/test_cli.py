import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest
from click.testing import CliRunner

from metablock.cli import main

BUNDLE = Path(__file__).parent / "bundle"
BLOCKS = Path(__file__).parent / "blocks"


def block_name(stem: str) -> str:
    """Block name unique to the running interpreter.

    The CI matrix runs the live suite on four Python versions at once. Applying
    the same block from every job makes their route rewrites collide: one job
    lists the block routes while another replaces them, and the API then 500s
    fetching the plugins of a route that no longer exists.
    """
    return f"{stem}-py{sys.version_info.major}{sys.version_info.minor}"


@pytest.fixture
def bundle(tmp_path: Path) -> Path:
    """A copy of the static bundle with the deploy timestamp filled in.

    The timestamp is injected here rather than committed, so the deployed page
    shows when it was shipped instead of a date that goes stale in the repo.
    """
    target = tmp_path / "bundle"
    shutil.copytree(BUNDLE, target)
    index = target / "index.html"
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    index.write_text(index.read_text().replace("__DEPLOYED_AT__", stamp))
    return target


def test_bundle_deploy_date(bundle: Path):
    """Guards the placeholder in index.html against being renamed"""
    html = (bundle / "index.html").read_text()
    assert "__DEPLOYED_AT__" not in html
    assert "UTC</time>" in html


def test_cli_apply_path_error():
    runner = CliRunner()
    result = runner.invoke(main, ["apply", "foo"])
    assert result.exit_code == 2
    assert "Invalid value for 'PATH': Path 'foo' does not exist" in result.output


def test_cli_apply_no_space():
    runner = CliRunner()
    result = runner.invoke(main, ["apply", "tests/blocks"])
    assert result.exit_code == 1
    assert result.output.startswith("metablock space is required")


@pytest.fixture
def blocks(tmp_path: Path) -> Path:
    """The block manifests, renamed so each interpreter applies its own block.

    `apply` takes the block name from the manifest filename, so the rename is
    all it takes to give every CI matrix job a block of its own.
    """
    target = tmp_path / "blocks"
    target.mkdir()
    for manifest in BLOCKS.glob("*.yaml"):
        (target / f"{block_name(manifest.stem)}.yaml").write_text(manifest.read_text())
    return target


def test_cli_apply(org_id: str, blocks: Path):
    runner = CliRunner()
    result = runner.invoke(
        main, ["apply", str(blocks), "--space", "mblock", "--org", org_id]
    )
    assert result.exit_code == 0
    # created on the first run against a new interpreter, updated afterwards
    assert result.output.rstrip().endswith(f"block {block_name('backend')}")


def test_cli_ship(ship_block_id: str, org_id: str, bundle: Path):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "ship",
            str(bundle),
            "--block-id",
            ship_block_id,
            "--name",
            "just a test",
            "--org",
            org_id,
        ],
    )
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert lines[0] == f"Created zip file: {bundle}.zip"
    assert lines[1] == f"shipped {bundle}.zip to test prod"
