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
karaulnykh-veronika
