.PHONY: help build clean clean-build setup setup-dev install release-check type-check flake8-check lint tests twine-release-test

.DEFAULT: help
help:
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
	python setup.py develop

setup-dev: clean
	virtualenv -p python3 venv
	./venv/bin/pip install -U pip
	./venv/bin/pip install -U setuptools twine bumpversion
	./venv/bin/python setup.py develop

install: clean
	python setup.py install

type-check:
	@echo ">>> checking types in ftoolz and tests"
	MYPYPATH=./stubs mypy ftoolz tests || ( echo ">>> type check failed"; exit 1; )

flake8-check:
	@echo ">>> enforcing PEP 8 style with flake8 in ftoolz and tests"
	flake8 --config=.flake8 ftoolz/ tests/ || ( echo ">>> flake8 check failed"; exit 1; )

lint:
	@echo ">>> linting code"
	pylint -j 0 --rcfile .pylintrc ftoolz tests || ( echo ">>> linting failed"; exit 1; )

tests:
	@echo ">>> running tests"
	python tests/run.py || ( echo ">>> tests failed"; exit 1; )
#	python setup.py test

release-check: type-check flake8-check lint tests

twine-release-test: build
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
