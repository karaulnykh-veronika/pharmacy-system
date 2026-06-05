# Pharmacy Management System

Система управления аптекой с графическим интерфейсом.

## О проекте

- Просмотр каталога лекарств с поиском
- Добавление товаров в корзину
- Оформление покупки с печатью чека
- Пополнение склада
- Возврат товаров по чеку
- Статистика продаж

## Структура
app/gui/ - графический интерфейс
packages/core/ - бизнес-логика (переиспользуемая)
tests/ - тесты
docs/ - документация и диаграммы

## Быстрый старт

```bash
git clone https://github.com/karaulnykh-veronika/pharmacy-system.git
cd pharmacy-system
make setup
make run

 ## Тестирование
make test        # запуск тестов
make coverage    # отчёт о покрытии

## Docker
make docker-build
make docker-up
make docker-down

## Документация
Спецификация

Архитектура

Диаграммы

## Автор
karaulnykh-veronika and Noise-of-Durka

## Работа с компонентом

```bash
make build-lib        # сборка пакета
make install-lib-local # локальная установка
make publish-lib      # публикация на TestPyPI

##  Работа с переиспользуемым компонентом

```bash
make build-lib        # сборка пакета из packages/core/
make install-lib-local # локальная установка компонента
make publish-lib      # публикация на TestPyPI (требуется регистрация)

## Тестирование

make test             # все тесты (unit)
make smoke-test       # smoke-тесты
make coverage         # отчёт о покрытии
make check-all        # полная проверка
## Docker
make docker-build     # сборка образа
make docker-up        # запуск контейнера
make docker-down      # остановка контейнера

## Очистка
make clean            # удаление временных файлов

##  Работа с переиспользуемым компонентом

```bash
make build-lib        # сборка пакета из packages/core/
make install-lib-local # локальная установка компонента
make publish-lib      # публикация на TestPyPI (требуется регистрация)

## Тестирование

make test             # все тесты (unit)
make smoke-test       # smoke-тесты
make coverage         # отчёт о покрытии
make check-all        # полная проверка
## Docker
make docker-build     # сборка образа
make docker-up        # запуск контейнера
make docker-down      # остановка контейнера

## Очистка
make clean            # удаление временных файлов
