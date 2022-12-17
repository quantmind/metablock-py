import asyncio

import pytest
from metablock import Metablock


@pytest.fixture(scope="module", autouse=True)
def event_loop():
    """Return an instance of the event loop."""
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


@pytest.fixture(scope="module")
async def cli():
    async with Metablock() as cli:
        yield cli
