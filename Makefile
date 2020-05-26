SHELL := /bin/bash

.PHONY: all driver clean remove_venv

all: venv driver

venv:
	python3 -m venv venv
	source venv/bin/activate && pip install -r requirements.txt

driver: venv
	wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
	tar xzf geckodriver-v0.26.0-linux64.tar.gz
	mv geckodriver venv/bin
	rm geckodriver-v0.26.0-linux64.tar.gz

clean:
	rm -rf venmo/logs
	rm venmo/geckodriver.log

remove_venv:
	rm -rf venv
