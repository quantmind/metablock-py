# Minimal makefile for Sphinx documentation
#

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
	rm -rf .coverage

.PHONY: install
install: 		## install packages with poetry
	@./.dev/install

.PHONY: lint
lint: 			## run linters
	poetry run ./.dev/lint fix

.PHONY: test
test:			## test with coverage
	@poetry run \
		pytest -v --cov --cov-report xml --cov-report html -x

.PHONY: test-lint
test-lint:		## run linters
	poetry run ./.dev/lint

.PHONY: publish
publish:		## release to pypi and github tag
	@poetry publish --build -u __token__ -p $(PYPI_TOKEN)

.PHONY: outdated
outdated:		## show outdated packages
	poetry show -o -a
