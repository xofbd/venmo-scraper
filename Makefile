SHELL := /bin/bash
ACTIVATE_VENV := source venv/bin/activate
SRC := ${wildcard requirements/requirements*.txt}

.PHONY: all install dev tests clean help

## all:                  Download browser driver and install the package locally
all: clean venv/bin/geckodriver install

## venv:                 Initialize virtual environment
venv: requirements/pip-tools.txt
	python3 -m venv $@
	${ACTIVATE_VENV} && pip install -r $<

## venv/bin/geckodriver: Download Firefox web driver
venv/bin/geckodriver: venv
	wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
	tar xzf geckodriver-v0.26.0-linux64.tar.gz
	mv geckodriver venv/bin
	rm geckodriver-v0.26.0-linux64.tar.gz
	touch venv/bin/geckodriver

## install:              Install package locally for usage
install: .install
.install: requirements/requirements.txt venv
	${ACTIVATE_VENV} && pip-sync $< && pip install .
	rm -f .dev
	touch $@

## dev:                  Configure the development environment for the package
dev: .dev
.dev: ${SRC} venv
	${ACTIVATE_VENV} && pip-sync ${SRC} && pip install -e .
	rm -f .install
	touch $@

## tests:                Run tests
tests: dev
	${ACTIVATE_VENV} && pytest -s tests

requirements: ${SRC}

requirements/%.txt: requirements/%.in
	${ACTIVATE_VENV} && pip-compile $<

requirements/requirement-dev.txt: requirements/requirements.txt

## clean:                Remove virtual env and all generated files and directories
clean:
	rm -f geckodriver.log
	rm -f .pip-tools .install .dev
	rm -rf venv
	rm -rf venmo_scraper.egg-info
	rm -rf .pytest_cache
	find . | grep __pycache__ | xargs rm -rf

help: Makefile
	@sed -n 's/^##//p' $<
