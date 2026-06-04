# Makefile for Pharmacy System (Windows compatible)
VENV := .venv
PYTHON := $(VENV)/Scripts/python
PIP := $(VENV)/Scripts/pip

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

run:
	$(PYTHON) -c "print('Tkinter app will go here')"

run-cli:
	$(PYTHON) app/cli/main.py

test:
	@echo "No tests yet"

clean:
	rm -rf $(VENV)
	rm -rf __pycache__
