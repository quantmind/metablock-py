# Minimal makefile for Sphinx documentation
#

.PHONY: help clean docs

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

clean:			## remove python cache files
	find . -name '__pycache__' | xargs rm -rf
	find . -name '*.pyc' -delete
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage


version:		## display software version
	@python setup.py --version


install: 		## install packages in virtualenv
	@./dev/install


lint: 			## run linters
	flake8
	isort .
	./dev/run-black


mypy:			## run mypy
	@mypy metablock


test:			## test with coverage
	@pytest --cov --cov-report xml --cov-report html


test-lint:		## run linters
	flake8
	isort . --check
	./dev/run-black --check


test-version:		## validate version with pypi
	@agilekit git validate


bundle3.6:		## build python 3.6 bundle
	@python setup.py bdist_wheel --python-tag py36

bundle3.7:		## build python 3.7 bundle
	@python setup.py bdist_wheel --python-tag py37

bundle3.8:		## build python 3.8 bundle
	@python setup.py sdist bdist_wheel --python-tag py38


release-github:		## new tag in github
	@agilekit git release --yes


release-pypi:		## release to pypi and github tag
	@twine upload dist/* --username lsbardel --password $(PYPI_PASSWORD)
