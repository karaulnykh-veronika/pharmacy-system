"""Фикстуры для тестов — примеры товаров и корзин"""
import pytest
from packages.core.models import Product, BasketItem

@pytest.fixture
def sample_products():
    """Список тестовых товаров"""
    return [
        Product(id=1, name="Аспирин", price=50, category_id=1, quantity_at_storage=100),
        Product(id=2, name="Парацетамол", price=30, category_id=1, quantity_at_storage=150),
        Product(id=3, name="Нурофен", price=120, category_id=1, quantity_at_storage=80),
    ]

@pytest.fixture
def sample_basket():
    """Тестовая корзина"""
    return [
        BasketItem(product_id=1, product_name="Аспирин", quantity=2, price_per_unit=50),
        BasketItem(product_id=2, product_name="Парацетамол", quantity=3, price_per_unit=30),
    ]
