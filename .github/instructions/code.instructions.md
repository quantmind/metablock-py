---
name: metablock-py code instructions
applyTo: "**"
description: Development guidance for the metablock python client - tooling, generated models, manager architecture, tests and conventions.
---

# metablock-py

Asynchronous Python client for the [metablock API](https://api.metablock.io/v1/docs),
published to PyPI as `metablock`.

## Tooling

This project uses **uv** for dependency management and packaging (hatchling build
backend). There is no `poetry.lock` and no `requirements.txt` — `uv.lock` is the
single source of truth and is committed.

```bash
make install      # ./.dev/install -> uv sync --all-extras --all-groups
make lint         # black + ruff + mypy, with fixes applied
make test-lint    # same, check mode only (what CI runs)
make test         # pytest with coverage
make models       # regenerate metablock/schema.py from the OpenAPI spec
make upgrade      # uv lock --upgrade
make outdated     # uv tree --outdated
make publish      # uv build && uv publish
```

Run one-off commands through the environment with `uv run`, e.g.
`uv run pytest tests/test_spaces.py -x`. Never `pip install` into `.venv`
directly; add the dependency to `pyproject.toml` and re-sync.

Dependencies are split three ways:

- `[project.dependencies]` — runtime (`httpx2`, `multidict`, `pydantic`)
- `[project.optional-dependencies] cli` — extras shipped to users (`pip install metablock[cli]`)
- `[dependency-groups] dev` — local/CI only, never published

## Layout

| Path | Purpose |
|---|---|
| `metablock/schema.py` | **generated** pydantic models — do not edit, see below |
| `metablock/client.py` | `Metablock` — the entry point; owns the `httpx2.AsyncClient`, the HTTP verbs and the managers |
| `metablock/components.py` | `Manager` base dataclass and the error types |
| `metablock/spaces.py` | `Spaces` and `Blocks` managers |
| `metablock/orgs.py` | `Orgs` manager (organizations and their roles) |
| `metablock/extensions.py` | `Extensions` (public) and `OrgExtensions` (`/orgs-extensions`) managers |
| `metablock/user.py` | `Users` manager |
| `metablock/utils.py` | `compact_dict`, `filter_as_tuple`, `temp_zipfile` helpers |
| `metablock/cli.py` | `metablock` console script (click), gated behind the `cli` extra |

## HTTP client

The transport is **`httpx2`**, not `httpx`. This is deliberate: `httpx2` is the
successor to `httpx` by the same author, maintained by Pydantic Services at
[pydantic/httpx2](https://github.com/pydantic/httpx2). It is not a typo and must
not be "corrected" back to `httpx`. The imported surface (`AsyncClient`,
`Response`, `.status_code`, `.json()`, `.raise_for_status()`) is API-compatible
with httpx, so the migration was import-only.

## Generated models

`metablock/schema.py` is generated from the API's OpenAPI spec by `.dev/models`
(`make models`). **Never edit it by hand** — change the script and regenerate.
Flag choices are documented in the script header; the two non-obvious ones are
`--disable-timestamp` (keeps regeneration diffs clean) and mapping `format: email`
to `str` (avoids an `email-validator` runtime dependency, and the spec gives
`OrgMember.org_email` a default of `""` which `EmailStr` would reject).

The spec is not a perfect description of the API, so expect gaps in both
directions and verify against the live API before trusting it:

- the API returns `User.status`, which the spec's `User` schema omits
- `Org.created` is required by the spec but absent from `/user/orgs` payloads

## Managers hold behaviour, models hold data

The models are plain data and carry no client reference. All behaviour lives in
manager dataclasses which subclass `Manager` (`cli` field, `path` ClassVar) and
compose their URL as `{cli.url}/{path}`.

`metablock/__init__.py` exports only `Metablock` and the two error types. Models
are imported from `metablock.schema`, managers from their own modules — do not
add re-exports to the package root.

```python
space  = await cli.spaces.get("my-space")     # -> schema.Space, plain data
blocks = await cli.spaces.blocks(space.id)    # parent id passed explicitly
```

When adding a resource:

- add a `@dataclass` manager subclassing `Manager` with a `path: ClassVar[str]`
- expose it as a property on `Metablock`
- take the parent identifier as the first argument for nested paths
- build query params with `compact_dict(...)` so `None` values are dropped
- annotate arguments with `Annotated[T, Doc(...)]` — these are public API docs

Models are never subclassed to add behaviour. An earlier design mixed the two by
having entities carry a `root` back-reference to the client; it was removed in
2.0 because the spec's own `root` and `url` fields on `Block` collided with it.

## Organization header

Most endpoints require an `x-metablock-org-id` header naming the organization the
request acts within. Set it with `Metablock(org_id=...)` or `METABLOCK_ORG_ID`;
the CLI takes `--org`. Requests that need it fail with a `422` when it is missing.

The org is **never** in the path: spaces are `/spaces`, not `/orgs/{org}/spaces`,
and org-owned extensions live at the sibling path `/orgs-extensions`. Only roles
(`/orgs/{org}/roles`) are still nested under the organization, and they take no
org header.

## Tests

`tests/` runs against the **live** metablock API — there are no mocks. A valid
`METABLOCK_API_TOKEN` is required; the root `conftest.py` calls
`dotenv.load_dotenv()`, so a local `.env` (gitignored) supplies it. Tests are
`asyncio_mode = "auto"`, so async test functions need no decorator, and the `cli`
fixture is module-scoped.

Because tests are live, a failure may reflect API state rather than a code bug —
check the response before assuming the client is wrong. Fixtures in
`tests/conftest.py` reference real objects (the `metablock` org, a fixed block id).
The `cli` fixture resolves that org and sets `client.org_id`, so tests send the
required organization header. The CLI tests are sync (click's `CliRunner` calls
`asyncio.run` itself, so they cannot be async) and take the id from the separate
`org_id` fixture.

## Conventions

- Python 3.11–3.14; the CI matrix covers all four
- `from __future__ import annotations` at the top of modules using forward refs
- full type annotations — mypy runs with `disallow_untyped_defs` on `metablock`
  and `tests` (relaxed to untyped-ok for `tests.*`)
- line length 88, black formatting, ruff with `A,E,W,F,I,B,N`
- ruff's `I` rule handles import sorting; do not add a separate isort pass
- `pyproject.toml` and `taplo.toml` are formatted by taplo, which reorders the
  `dependency-groups.dev` and `project.optional-dependencies.cli` arrays

## Release

Releases are driven by `v*` tags and `make release` — see
[release.instructions.md](./release.instructions.md). `version` in
`pyproject.toml` is the single source of truth: `__version__` reads it back at
runtime with `importlib.metadata.version("metablock")`, so there is nothing else
to bump.
