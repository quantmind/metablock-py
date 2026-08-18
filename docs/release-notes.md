# Release notes

## v2.0.1

The `ship` command takes a `--timeout` option, defaulting to `METABLOCK_API_TIMEOUT` (60 seconds), replacing the hardcoded 10 second upload timeout.

[Full changelog](https://github.com/quantmind/metablock-py/compare/v2.0.0...v2.0.1)

## v2.0.0

A ground-up rework of the client. Data models are now generated from the API's
OpenAPI spec instead of being maintained by hand, and behaviour has moved out of
the models into manager classes, so a model is plain data and never holds a
reference to the client. The API itself also changed: the organization is now
selected by a header rather than by the URL. Almost every call site changes —
see **Breaking changes** below before upgrading.

### Breaking changes

- Models are generated from the OpenAPI spec into `metablock.schema` and are
  plain pydantic models. The `MetablockComponent` / `MetablockEntity` classes and
  their `root` / `root_path` fields are gone, so entities no longer chain:
  `space.blocks.get_list()` becomes `cli.spaces.blocks(space.id)`, and
  `block.ship(...)` becomes `cli.blocks.ship(block.id, ...)`.
- Behaviour lives in manager dataclasses reachable from the client: `cli.spaces`,
  `cli.blocks`, `cli.orgs`, `cli.extensions`, `cli.org_extensions`, `cli.user`.
- `cli.get_user()` / `cli.update_user()` / `cli.delete_user()` are replaced by
  `cli.user.get()` / `cli.user.update()` / `cli.user.delete()`.
- Spaces are no longer scoped by URL: `GET /orgs/{org}/spaces` became
  `GET /spaces`, so `org.spaces.get_list()` becomes `cli.spaces.get_list()`.
- Organization extensions moved to the sibling path `/orgs-extensions` and are
  managed through `cli.org_extensions`.
- Most endpoints now require an `x-metablock-org-id` header naming the
  organization the request acts within. Set it with `Metablock(org_id=...)`, the
  `METABLOCK_ORG_ID` environment variable, or `--org` on the CLI. Requests that
  need it fail with a `422` when it is missing.
- `metablock/__init__.py` exports only `Metablock`, `MetablockError` and
  `MetablockResponseError`. Import models from `metablock.schema` and managers
  from their own modules.
- The transport is now `httpx2` rather than `httpx`.
- Endpoints that no longer exist on the API were removed: `Domains.check()`,
  `Org.add_info()`, `User.get_permissions()`, `User.check_password()`, the
  `Orgs.get_list()` listing, and the empty organization members and roles stubs.
  Roles are now implemented against the real `/orgs/{org}/roles` endpoints.

### New features

- `metablock.schema` covers the whole documented API surface, including
  resources the client did not previously model such as servers, dashboards,
  peerings and API tokens.
- `make models` regenerates the models from the live spec via `.dev/models`.
- New organization operations: `cli.orgs.update()` and the full role set
  (`roles`, `get_role`, `create_role`, `update_role`, `delete_role`).
- `cli.org_extensions.get_list()` supports `name`, `search`, `limit` and
  `cursor` filters, and `cli.spaces.get_list()` / `cli.spaces.create()` operate
  on the organization selected by the client.
- User API tokens are exposed through `cli.user.tokens()`, `create_token()` and
  `delete_token()`.
- The CLI takes a `--org` option on both `apply` and `ship`.

### Improvements and fixes

- Added coverage for certificate retrieval, block deployments, space
  nameservers, organization roles and user API tokens, which the client
  exposed but never exercised.
- Fixed the `422` failures caused by the missing organization header.
- Packaging moved from poetry to uv with the hatchling build backend;
  `uv.lock` replaces `poetry.lock` and the dev dependencies moved to a PEP 735
  dependency group so they are no longer published.
- `black` is pinned to `target-version = py311` so formatting is identical
  across the whole supported Python range instead of varying with the
  interpreter running it.
- `make publish` clears `dist/` before building, so a stale artefact from an
  earlier version can no longer be uploaded.
- Releases are now driven by `v*` tags through `.github/workflows/release.yml`
  and `make release`, replacing the `release` commit-message trigger.

### Documentation and assets

- The readme documents the manager API and the organization header.
- Repository guidance moved to `.github/instructions/`, with `CLAUDE.md`
  referencing it.

[Full changelog](https://github.com/quantmind/metablock-py/compare/v1.2.0...v2.0.0)
