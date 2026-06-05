"""Smoke-тесты: проверяют, что приложение импортируется и основные функции работают"""
import sys
import os

# Добавляем корневую папку проекта в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from packages.core.services import (
    validate_quantity,
    find_product_by_name,
    check_stock_availability,
    calculate_item_total
)
from packages.core.models import Product, BasketItem

def test_core_imports():
    """Проверка, что все core-модули импортируются"""
    from packages.core import models, services, interfaces, repositories
    assert models is not None
    assert services is not None

def test_validate_quantity_smoke():
    """Базовая проверка работы функции валидации"""
    validate_quantity(5)  # не должно быть ошибки

def test_calculate_item_total_smoke():
    """Базовая проверка расчёта суммы"""
    result = calculate_item_total(100, 3)
    assert result == 300

def test_find_product_by_name_smoke():
    """Базовая проверка поиска товара"""
    products = [
        Product(id=1, name="Аспирин", price=50, category_id=1, quantity_at_storage=100),
        Product(id=2, name="Парацетамол", price=30, category_id=1, quantity_at_storage=150),
    ]
    found = find_product_by_name(products, "Аспирин")
    assert found is not None
    assert found.name == "Аспирин"

def test_check_stock_availability_smoke():
    """Базовая проверка наличия товара"""
    product = Product(id=1, name="Аспирин", price=50, category_id=1, quantity_at_storage=100)
    assert check_stock_availability(product, 50) is True
    assert check_stock_availability(product, 150) is False

def test_basket_item_total_price():
    """Проверка расчёта суммы позиции в корзине"""
    item = BasketItem(product_id=1, product_name="Аспирин", quantity=3, price_per_unit=50)
    assert item.total_price == 150
