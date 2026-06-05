# Добро пожаловать в Pharmacy Management System

Система управления аптекой с графическим интерфейсом.

## Возможности

- Просмотр каталога лекарств с поиском
- Добавление товаров в корзину
- Оформление покупки с печатью чека
- Пополнение склада
- Возврат товаров по чеку
- Статистика продаж

## Быстрый старт

```bash
git clone https://github.com/karaulnykh-veronika/pharmacy-system.git
cd pharmacy-system
make setup
make run
Архитектура
app/gui/ — графический интерфейс

packages/core/ — бизнес-логика

tests/ — тесты
