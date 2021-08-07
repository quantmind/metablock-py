import asyncio

import pytest
from metablock import Metablock


@pytest.fixture(scope="session")
def loop():
    """Return an instance of the event loop."""
    # Shared loop makes everything easier. Just don't mess it up.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def cli(loop):
    async with Metablock() as cli:
        yield cli
