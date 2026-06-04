VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

.PHONY: help setup run test clean

help:
	@echo "Available commands:"
	@echo "  make setup      - Create virtual environment"
	@echo "  make run        - Run the pharmacy application"
	@echo "  make test       - Run all tests"
	@echo "  make clean      - Remove virtual environment"

setup:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip

run:
	$(PYTHON) -c "print('Pharmacy app will go here')"

test:
	@echo "No tests yet"

clean:
	rm -rf $(VENV)
