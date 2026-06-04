"""Smoke tests to verify the application starts correctly."""

import sys
from pathlib import Path

# Добавляем путь к src
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))


def test_import_pharmacy_modules():
    """All core modules should import without errors."""
    try:
        from pharmacy import models
        from pharmacy import business
        from pharmacy import database
    except ImportError as e:
        assert False, f"Import failed: {e}"


def test_models_module_has_required_classes():
    """Models module should contain all data classes."""
    from pharmacy.models import Product, CartItem, ShoppingCart, ProductCategory
    
    # Проверяем, что классы существуют
    assert Product is not None
    assert CartItem is not None
    assert ShoppingCart is not None
    assert ProductCategory is not None


def test_business_module_has_required_classes():
    """Business module should contain pricing and validation classes."""
    from pharmacy.business import PricingEngine, QuantityValidator
    
    assert PricingEngine is not None
    assert QuantityValidator is not None


def test_database_module_has_database_class():
    """Database module should contain PharmacyDatabase class."""
    from pharmacy.database import PharmacyDatabase
    
    assert PharmacyDatabase is not None


def test_can_create_product():
    """Should be able to create a Product instance."""
    from pharmacy.models import Product
    from decimal import Decimal
    
    product = Product(
        id=1,
        name="Test Medicine",
        price=Decimal("100.00"),
        category_id=1,
        quantity_in_stock=50
    )
    
    assert product.id == 1
    assert product.name == "Test Medicine"
    assert product.price == Decimal("100.00")
    assert product.quantity_in_stock == 50


def test_can_create_shopping_cart():
    """Should be able to create a ShoppingCart and add items."""
    from pharmacy.models import Product, CartItem, ShoppingCart
    from decimal import Decimal
    
    cart = ShoppingCart()
    assert cart.item_count == 0
    assert cart.total == Decimal(0)
    
    item = CartItem(
        product_id=1,
        product_name="Test",
        quantity=2,
        price=Decimal("50.00")
    )
    cart.add_item(item)
    
    assert cart.item_count == 1
    assert cart.total == Decimal("100.00")
