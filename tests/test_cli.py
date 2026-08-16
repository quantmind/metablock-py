import shutil
from datetime import datetime, timezone
from pathlib import Path

import pytest
from click.testing import CliRunner

from metablock.cli import main

BUNDLE = Path(__file__).parent / "bundle"


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


def test_cli_apply(org_id: str):
    runner = CliRunner()
    result = runner.invoke(
        main, ["apply", "tests/blocks", "--space", "mblock", "--org", org_id]
    )
    assert result.exit_code == 0
    assert result.output.endswith("updated block backend\n")


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
