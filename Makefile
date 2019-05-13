.PHONY: help build clean setup setup-system install install-system release-check type-check flake8-check lint tests twine-release-test

.DEFAULT: help
help:
	@echo "make [py=/path/to/python] build"
	@echo "       build distribution directories"
	@echo "make clean"
	@echo "       clean distribution directories"
	@echo "make [py=/path/to/python] setup"
	@echo "       setup development environment, optionally using provided python"
	@echo "make setup-system"
	@echo "       setup development environment using system python"
	@echo "make [py=/path/to/python] install"
	@echo "       install dependencies, optionally using provided python"
	@echo "make install-system"
	@echo "       install dependencies using system python"
	@echo "make [py=/path/to/python] type-check"
	@echo "       run mypy type checking"
	@echo "make [py=/path/to/python] flake8-check"
	@echo "       run flake8 code style check"
	@echo "make [py=/path/to/python] lint"
	@echo "       run pylint"
	@echo "make [py=/path/to/python] tests"
	@echo "       run unit and doc tests"
	@echo "make [py=/path/to/python] coverage-check"
	@echo "       run test coverage check"
	@echo "make [py=/path/to/python] release-check"
	@echo "       run type-check, flake8 check, linting, tests and coverage check"
	@echo "make [py=/path/to/python] twine-release-test"
	@echo "       release ftoolz to test pypi using twine"

build: clean
	@echo ">>> building ftoolz distribution"
	pipenv $(if $(py),--python $(py) --site-packages ,)run build

clean:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

setup:
	pipenv install --dev $(if $(py),--python $(py),)

setup-system:
	pipenv install --dev --system --deploy

install:
	pipenv install $(if $(py),--python $(py),)

install-system:
	pipenv install --system --deploy

type-check:
	@echo ">>> checking types in ftoolz and tests"
	pipenv $(if $(py),--python $(py) --site-packages ,)run type-check || ( echo ">>> type check failed"; exit 1; )

flake8-check:
	@echo ">>> enforcing PEP 8 style with flake8 in ftoolz and tests"
	pipenv $(if $(py),--python $(py) --site-packages ,)run flake8-check || ( echo ">>> flake8 check failed"; exit 1; )

lint:
	@echo ">>> linting code"
	pipenv $(if $(py),--python $(py) --site-packages ,)run lint || ( echo ">>> linting failed"; exit 1; )

tests:
	@echo ">>> running tests"
	pipenv $(if $(py),--python $(py) --site-packages ,)run tests || ( echo ">>> tests failed"; exit 1; )

release-check: type-check flake8-check lint tests

twine-release-test: build
	pipenv $(if $(py),--python $(py) --site-packages ,)run release-test
