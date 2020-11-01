SHELL := /bin/bash

.PHONY: all driver tests clean

all: clean venv venv/bin/geckodriver

venv: requirements.txt
	test -d venv || python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	touch venv

venv/bin/geckodriver: venv
	wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
	tar xzf geckodriver-v0.26.0-linux64.tar.gz
	mv geckodriver venv/bin
	rm geckodriver-v0.26.0-linux64.tar.gz
	touch venv/bin/geckodriver

driver:
	make venv/bin/geckodriver

tests:
	source venv/bin/activate && pytest tests

clean:
	rm -f geckodriver.log
	rm -rf venv
	rm -rf venmo_scraper.egg-info
	find . | grep __pycache__ | xargs rm -rf
