import zipfile
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Hashable, Iterable, Iterator

from multidict import MultiDict

DEFAULT_SKIP_VALUES = frozenset((None,))


def as_dict(data: Any, key: str = "data") -> dict:
    return {key: data} if not isinstance(data, dict) else data


def as_params(*, params: dict | None = None, **kwargs: Any) -> MultiDict:
    d = MultiDict(params if params is not None else {})
    d.update(kwargs)
    return d


def compact_dict(
    *args: Iterable[Any],
    skip_values: set[Any] | frozenset[Any] = DEFAULT_SKIP_VALUES,
    **kwargs: Any,
) -> dict[str, Any]:
    return {
        k: v
        for k, v in dict(*args, **kwargs).items()
        if isinstance(v, bool) or not isinstance(v, Hashable) or v not in skip_values
    }


@contextmanager
def temp_zipfile(path: str | Path) -> Iterator[Path]:
    """Create a temporary zip file."""
    p = Path(path)
    if not p.is_dir():
        raise ValueError(f"Path {p} is not a directory")

    # Create a zip file from the directory
    zip_path = p.with_suffix(".zip")
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in p.rglob("*"):  # Recursively add all files in the directory
                arcname = file.relative_to(p)  # Preserve relative paths in the archive
                zipf.write(file, arcname)
        yield zip_path
    finally:
        # Clean up the zip file after shipping
        if zip_path.exists():
            zip_path.unlink()
