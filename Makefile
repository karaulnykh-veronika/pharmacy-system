.PHONY: help setup run test clean

help:
	@echo "Доступные команды:"
	@echo "  make setup  - установка зависимостей"
	@echo "  make run    - запуск приложения"
	echo "  make test   - запуск тестов"
	@echo "  make clean  - удаление временных файлов"

setup:
	pip install -r requirements.txt

run:
	python app/gui/main_window.py

test:
	pytest tests/ -v

clean:
	rm -rf __pycache__ .pytest_cache .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
