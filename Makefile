.PHONY: help
help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: clean
clean:			## remove python cache files
	find . -name '__pycache__' | xargs rm -rf
	find . -name '*.pyc' -delete
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	rm -rf .coverage

.PHONY: install
install: 		## install packages with uv
	@./.dev/install

.PHONY: lint
lint: 			## run linters and fix
	@./.dev/lint fix

.PHONY: models
models:			## regenerate metablock/schema.py from the OpenAPI spec
	@./.dev/models

.PHONY: outdated
outdated:		## show outdated packages
	uv tree --outdated

.PHONY: publish
publish:		## release to pypi and github tag
	@rm -rf dist
	@uv build
	@uv publish --token $(PYPI_TOKEN)

.PHONY: release
release:		## tag current version (from pyproject.toml) and push
	$(eval VERSION := $(shell grep '^version' pyproject.toml | head -1 | sed 's/version = "\(.*\)"/\1/'))
	@read -p "Tagging with v$(VERSION), are you sure? [Y/n] " ans; \
	ans=$${ans:-Y}; \
	if [ "$$ans" = "Y" ] || [ "$$ans" = "y" ]; then \
		git tag -a v$(VERSION) -m "v$(VERSION)" && git push origin v$(VERSION); \
	else \
		echo "Aborted."; \
	fi

.PHONY: test
test:			## test with coverage
	@uv run \
		pytest -v --cov --cov-report xml --cov-report html -x

.PHONY: test-lint
test-lint:		## run linters in check mode
	@./.dev/lint

.PHONY: upgrade
upgrade:		## upgrade locked dependencies
	uv lock --upgrade
