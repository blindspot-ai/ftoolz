.PHONY: help build clean clean-build setup setup-dev install release-check type-check flake8-check lint tests release-build release-test twine-release-test

VERSION := $(shell sed -ne 's/^\s*version=.*\([0-9]\+\.[0-9]\+\.[0-9]\+\).*/\1/p' setup.py)

.DEFAULT: help
help:
	@echo "ftoolz v$(VERSION):"
	@echo "==================="
	@echo "make build"
	@echo "       build distribution directories"
	@echo "make clean"
	@echo "       clean virtual environment and distribution"
	@echo "make clean-build"
	@echo "       clean distribution directories"
	@echo "make setup"
	@echo "       setup development environment"
	@echo "make setup-dev"
	@echo "       setup virtualenv and development environment"
	@echo "make install"
	@echo "       install dependencies"
	@echo "make type-check"
	@echo "       run mypy type checking"
	@echo "make flake8-check"
	@echo "       run flake8 code style check"
	@echo "make lint"
	@echo "       run pylint"
	@echo "make tests"
	@echo "       run unit and doc tests"
	@echo "make release-check"
	@echo "       run type-check, flake8 check, linting and tests"
	@echo "make release-build"
	@echo "       run release-check and build"
	@echo "make release-test"
	@echo "       build docker image with ftoolz installation and distribution"
	@echo "make twine-release-test"
	@echo "       release ftoolz to test pypi using twine"

build: clean-build
	@echo ">>> building ftoolz distribution"
	python setup.py sdist

clean: clean-build
	rm -rf venv

clean-build:
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

setup: clean
	pip install -U -e .[dev,test]

setup-dev: clean
	virtualenv -p python3 venv
	./venv/bin/pip install -U pip
	./venv/bin/pip install -U setuptools
	./venv/bin/pip install -U -e .[dev,test]

install: clean
	python setup.py install

type-check:
	@echo ">>> checking types in ftoolz and tests"
	mypy ftoolz tests || ( echo ">>> type check failed"; exit 1; )

flake8-check:
	@echo ">>> enforcing PEP 8 style with flake8 in ftoolz and tests"
	flake8 --config=.flake8 ftoolz/ tests/ || ( echo ">>> flake8 check failed"; exit 1; )

lint:
	@echo ">>> linting code"
	pylint -j 0 --rcfile .pylintrc ftoolz tests || ( echo ">>> linting failed"; exit 1; )

tests:
	@echo ">>> running tests"
	python3 tests/run.py || ( echo ">>> tests failed"; exit 1; )

release-check: type-check flake8-check lint tests

release-build: release-check build

release-test:
	@echo ">>> building docker image 'ftoolz:$(VERSION)-dev'"
	docker build --rm -t ftoolz:$(VERSION)-dev .

twine-release-test: build
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
