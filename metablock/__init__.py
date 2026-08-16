from importlib.metadata import version

from .client import Metablock
from .components import MetablockError, MetablockResponseError

__version__ = version("metablock")


__all__ = [
    "Metablock",
    "MetablockError",
    "MetablockResponseError",
]
