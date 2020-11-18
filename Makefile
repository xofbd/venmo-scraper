SHELL := /bin/bash
ACTIVATE_VENV := source venv/bin/activate

.PHONY: all install tests clean

all: clean venv/bin/geckodriver install

venv:
	test -d venv || python3 -m venv venv

venv/bin/geckodriver: venv
	wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
	tar xzf geckodriver-v0.26.0-linux64.tar.gz
	mv geckodriver venv/bin
	rm geckodriver-v0.26.0-linux64.tar.gz
	touch venv/bin/geckodriver

.pip-tools: venv requirements/pip-tools.txt
	${ACTIVATE_VENV} && \
	pip install -r requirements/pip-tools.txt
	touch .pip-tools

install:
	make .install

.install: .pip-tools requirements/requirements.txt
	${ACTIVATE_VENV} && \
	pip-sync requirements/requirements.txt && \
	pip install -e .
	rm -f .dev
	touch .install

dev:
	make .dev

.dev: venv .pip-tools requirements/requirements*.txt
	${ACTIVATE_VENV} && \
	pip-sync requirements/requirements.txt requirements/requirements-dev.txt
	pip install -e .
	rm -f .install
	touch .dev

tests: dev
	${ACTIVATE_VENV} && pytest tests

requirements/requirements.txt: .pip-tools requirements/requirements.in
	${ACTIVATE_VENV} && pip-compile requirements/requirements.in

requirements/requirements-dev.txt: .pip-tools requirements/requirements-dev.in
	${ACTIVATE_VENV} && pip-compile requirements/requirements-dev.in

clean:
	rm -f geckodriver.log
	rm -f .pip-tools
	rm -f .install
	rm -f .dev
	rm -rf venv
	rm -rf venmo_scraper.egg-info
	rm -rf .pytest_cache
	find . | grep __pycache__ | xargs rm -rf
