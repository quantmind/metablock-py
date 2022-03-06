import asyncio

import pytest
from metablock import Metablock


@pytest.fixture(scope="module")
def event_loop():
    """Return an instance of the event loop."""
    # Shared loop makes everything easier. Just don't mess it up.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def cli():
    async with Metablock() as cli:
        yield cli
