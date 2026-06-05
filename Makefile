.PHONY: help setup install-dev run test coverage clean docs docker-build docker-up docker-down check lint

PYTHON = python
APP_PATH = app/gui/main_window.py

help:
	@echo "Доступные команды:"
	@echo "  make setup         - установка зависимостей"
	@echo "  make install-dev   - установка зависимостей для разработки"
	@echo "  make run           - запуск GUI приложения"
	@echo "  make test          - запуск тестов"
	@echo "  make coverage      - отчёт о покрытии"
	@echo "  make docs          - сборка документации"
	@echo "  make docker-build  - сборка Docker образа"
	@echo "  make docker-up     - запуск контейнера"
	@echo "  make docker-down   - остановка контейнера"
	@echo "  make clean         - удаление временных файлов"
	@echo "  make check         - полная проверка (тесты + покрытие)"
	@echo "  make lint          - проверка стиля кода"

setup:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install pytest pytest-cov flake8 black

run:
	$(PYTHON) $(APP_PATH)

test:
	pytest tests/ -v

coverage:
	pytest tests/ --cov=packages/core --cov-report=html --cov-report=term
	@echo "📊 Отчёт: открыть coverage/index.html"

docs:
	@echo "📚 Документация в docs/specification.md и docs/architecture.md"
	@echo "📊 Диаграммы в docs/diagrams/ (Mermaid)"

docker-build:
	docker build -t pharmacy-system:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	rm -rf __pycache__ .pytest_cache .coverage coverage_html_report
	rm -rf *.pyc *.pyo
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

check: test coverage
	@echo "✅ Все проверки пройдены!"

lint:
	@flake8 packages/ app/ --max-line-length=120 --ignore=E501 2>/dev/null || echo "  Установите flake8: pip install flake8"
