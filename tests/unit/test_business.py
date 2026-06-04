"""Unit tests for business logic module."""

import sys
from pathlib import Path

# Добавляем src в путь поиска модулей
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from decimal import Decimal
from pharmacy.business import PricingEngine, QuantityValidator, DiscountResult


class TestPricingEngine:
    """Tests for pricing and discount calculations."""
    
    def test_calculate_total_empty(self):
        """Empty list should return zero."""
        result = PricingEngine.calculate_total([])
        assert result == Decimal(0)
    
    def test_calculate_total_single_item(self):
        """Single item calculation."""
        items = [(Decimal("100"), 2)]
        result = PricingEngine.calculate_total(items)
        assert result == Decimal(200)
    
    def test_calculate_total_multiple_items(self):
        """Multiple items calculation."""
        items = [(Decimal("100"), 2), (Decimal("50"), 3)]
        result = PricingEngine.calculate_total(items)
        assert result == Decimal(350)
    
    def test_apply_promo_discount_valid(self):
        """Valid promo code applies discount."""
        result = PricingEngine.apply_promo_discount(Decimal("1000"), "STUDENT10")
        assert result.percent == 10.0
        assert result.amount == Decimal("100")
        assert "Promo code STUDENT10" in result.reason
    
    def test_apply_promo_discount_invalid(self):
        """Invalid promo code gives no discount."""
        result = PricingEngine.apply_promo_discount(Decimal("1000"), "INVALID")
        assert result.percent == 0.0
        assert result.amount == Decimal(0)
    
    def test_apply_promo_discount_none(self):
        """No promo code gives no discount."""
        result = PricingEngine.apply_promo_discount(Decimal("1000"), None)
        assert result.percent == 0.0
        assert result.amount == Decimal(0)
    
    def test_apply_bulk_discount_less_than_10(self):
        """Less than 10 items: no bulk discount."""
        result = PricingEngine.apply_bulk_discount(Decimal("1000"), 5)
        assert result.percent == 0.0
        assert result.amount == Decimal(0)
    
    def test_apply_bulk_discount_10_or_more(self):
        """10 or more items: 15% bulk discount."""
        result = PricingEngine.apply_bulk_discount(Decimal("1000"), 10)
        assert result.percent == 15.0
        assert result.amount == Decimal("150")
    
    def test_calculate_final_price_no_discounts(self):
        """No discounts applied."""
        final, discounts = PricingEngine.calculate_final_price(
            subtotal=Decimal("1000"),
            total_quantity=1,
            promo_code=None
        )
        assert final == Decimal("1000")
        assert len(discounts) == 0
    
    def test_calculate_final_price_with_promo_only(self):
        """Only promo discount applied."""
        final, discounts = PricingEngine.calculate_final_price(
            subtotal=Decimal("1000"),
            total_quantity=1,
            promo_code="STUDENT10"
        )
        assert final == Decimal("900")
        assert len(discounts) == 1
        assert discounts[0].percent == 10.0
    
    def test_calculate_final_price_with_bulk_only(self):
        """Only bulk discount applied."""
        final, discounts = PricingEngine.calculate_final_price(
            subtotal=Decimal("1000"),
            total_quantity=10,
            promo_code=None
        )
        assert final == Decimal("850")
        assert len(discounts) == 1
        assert discounts[0].percent == 15.0
    
    def test_calculate_final_price_with_both_discounts(self):
        """Both promo and bulk discounts applied."""
        final, discounts = PricingEngine.calculate_final_price(
            subtotal=Decimal("1000"),
            total_quantity=10,
            promo_code="STUDENT10"
        )
        # First 10% = 900, then 15% of 900 = 135, final = 765
        assert final == Decimal("765")
        assert len(discounts) == 2


class TestQuantityValidator:
    """Tests for quantity validation."""
    
    def test_validate_positive_valid(self):
        """Positive quantity is valid."""
        valid, msg = QuantityValidator.validate_positive(5)
        assert valid is True
        assert msg == ""
    
    def test_validate_positive_zero(self):
        """Zero quantity is invalid."""
        valid, msg = QuantityValidator.validate_positive(0)
        assert valid is False
        assert "greater than 0" in msg
    
    def test_validate_positive_negative(self):
        """Negative quantity is invalid."""
        valid, msg = QuantityValidator.validate_positive(-5)
        assert valid is False
        assert "greater than 0" in msg
    
    def test_validate_stock_sufficient(self):
        """Sufficient stock is valid."""
        valid, msg = QuantityValidator.validate_stock(requested=5, available=10)
        assert valid is True
        assert msg == ""
    
    def test_validate_stock_insufficient(self):
        """Insufficient stock is invalid."""
        valid, msg = QuantityValidator.validate_stock(requested=15, available=10)
        assert valid is False
        assert "Insufficient stock" in msg
    
    def test_validate_stock_zero_requested(self):
        """Zero requested is invalid."""
        valid, msg = QuantityValidator.validate_stock(requested=0, available=10)
        assert valid is False
    
    def test_validate_return_valid(self):
        """Valid return quantity."""
        valid, msg = QuantityValidator.validate_return(
            requested=5, sold=10, already_returned=2
        )
        assert valid is True
        assert msg == ""
    
    def test_validate_return_too_much(self):
        """Return more than available is invalid."""
        valid, msg = QuantityValidator.validate_return(
            requested=10, sold=10, already_returned=5
        )
        assert valid is False
        assert "Cannot return" in msg
