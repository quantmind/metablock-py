from typing import Any

from .components import CrudComponent, MetablockEntity
from .spaces import BlockPlugin


# Extension
class Extension(MetablockEntity):
    """Object representing an Extension"""


class Extensions(CrudComponent[Extension]):
    """Extensions"""


# Plugin
class Plugin(MetablockEntity):
    """Object representing an Plugin"""

    async def blocks(self, **kwargs: Any) -> list[BlockPlugin]:
        return await self.cli.get(f"{self.url}/services", **kwargs)


class Plugins(CrudComponent[Plugin]):
    """Plugins"""
