SHELL = /usr/bin/env bash

.DEFAULT_GOAL := help
.PHONY: help
.PHONY: clean clean-build clean-pyc clean-test
.PHONY: lint test test-all test-coverage test-coverage-report-console test-coverage-report-html
.PHONY: dist install

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


help:
	@echo "Read README.md"
	@echo ""
	@echo "Makefile tasks:"
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, lint, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -rf .eggs/
	rm -rf build/
	rm -rf dist/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

clean-test: ## remove test, lint and coverage artifacts
	rm -rf .cache/
	rm -rf .tox/
	rm -f .coverage
	rm -rf htmlcov/
	rm -rf test-reports/
	rm -rf .mypy_cache/

lint: ## run tools for code style analysis, static type check, etc
	flake8 --config=setup.cfg  fd_gcp  tests
	mypy --config-file setup.cfg  fd_gcp

test: ## run tests
	python setup.py test

test-all: ## run tests on every Python version with tox
	@echo "TODO: configure tox"

test-coverage: ## run tests and record test coverage
	coverage run --rcfile=setup.cfg setup.py test

test-coverage-report-console: ## print test coverage summary
	coverage report --rcfile=setup.cfg -m

test-coverage-report-html: ## generate test coverage HTML report
	coverage html --rcfile=setup.cfg

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install
