from typing import Any

from multidict import MultiDict


def as_dict(data: Any, key: str = "data") -> dict:
    return {key: data} if not isinstance(data, dict) else data


def as_params(*, params: dict | None = None, **kwargs: Any) -> MultiDict:
    d = MultiDict(params if params is not None else {})
    d.update(kwargs)
    return d
