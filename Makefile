# Makefile for Pharmacy System (Windows compatible)
VENV := .venv
PYTHON := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip
PYTEST := $(VENV)/Scripts/pytest

.PHONY: help setup run run-cli test clean

help:
	@echo "Available commands:"
	@echo "  make setup      - Create virtual environment"
	@echo "  make run        - Run the pharmacy application (Tkinter)"
	@echo "  make run-cli    - Run CLI demo"
	@echo "  make test       - Run tests"
	@echo "  make clean      - Remove virtual environment"

setup:
	python -m venv $(VENV)
	-$(PIP) install --upgrade pip
	$(PIP) install pytest pytest-cov

run:
	$(PYTHON) -c "print('Tkinter app will go here')"

run-cli:
	$(PYTHON) app/cli/main.py

test:
	$(PYTEST) tests/ -v

clean:
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf .pytest_cache
