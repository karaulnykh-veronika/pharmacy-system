"""Pure business logic for pharmacy operations."""

from decimal import Decimal
from typing import List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class DiscountResult:
    """Result of discount calculation."""
    percent: float
    amount: Decimal
    reason: str


class PricingEngine:
    """Handles all price and discount calculations."""
    
    STUDENT_PROMO = "STUDENT10"
    PHARMACY_PROMO = "PHARMACY15"
    PENSION_PROMO = "PENSION20"
    
    DISCOUNT_RULES = {
        STUDENT_PROMO: 10.0,
        PHARMACY_PROMO: 15.0,
        PENSION_PROMO: 20.0,
    }
    
    @classmethod
    def calculate_total(cls, items: List[Tuple[Decimal, float]]) -> Decimal:
        """Calculate total price for list of (price, quantity) pairs."""
        total = Decimal(0)
        for price, quantity in items:
            total += price * Decimal(str(quantity))
        return total
    
    @classmethod
    def apply_promo_discount(cls, total: Decimal, promo_code: Optional[str] = None) -> DiscountResult:
        """Apply promotion discount if valid."""
        if not promo_code:
            return DiscountResult(percent=0.0, amount=Decimal(0), reason="No promo code")
        
        percent = cls.DISCOUNT_RULES.get(promo_code, 0.0)
        if percent > 0:
            amount = total * Decimal(str(percent / 100))
            return DiscountResult(percent=percent, amount=amount, reason=f"Promo code {promo_code}")
        
        return DiscountResult(percent=0.0, amount=Decimal(0), reason="Invalid promo code")
    
    @classmethod
    def apply_bulk_discount(cls, total: Decimal, total_quantity: float) -> DiscountResult:
        """Apply bulk purchase discount (15% for 10+ items)."""
        if total_quantity >= 10:
            percent = 15.0
            amount = total * Decimal(str(percent / 100))
            return DiscountResult(percent=percent, amount=amount, reason="Bulk purchase (10+ items)")
        return DiscountResult(percent=0.0, amount=Decimal(0), reason="No bulk discount")
    
    @classmethod
    def calculate_final_price(
        cls,
        subtotal: Decimal,
        total_quantity: float,
        promo_code: Optional[str] = None
    ) -> Tuple[Decimal, List[DiscountResult]]:
        """Calculate final price after all applicable discounts."""
        applied_discounts = []
        current_price = subtotal
        
        promo_discount = cls.apply_promo_discount(current_price, promo_code)
        if promo_discount.percent > 0:
            applied_discounts.append(promo_discount)
            current_price -= promo_discount.amount
        
        bulk_discount = cls.apply_bulk_discount(current_price, total_quantity)
        if bulk_discount.percent > 0:
            applied_discounts.append(bulk_discount)
            current_price -= bulk_discount.amount
        
        return current_price, applied_discounts


class QuantityValidator:
    """Validates product quantities."""
    
    @staticmethod
    def validate_positive(quantity: float) -> Tuple[bool, str]:
        if quantity <= 0:
            return False, "Quantity must be greater than 0"
        return True, ""
    
    @staticmethod
    def validate_stock(requested: float, available: float) -> Tuple[bool, str]:
        if requested <= 0:
            return False, "Quantity must be greater than 0"
        if requested > available:
            return False, f"Insufficient stock. Available: {available}"
        return True, ""
    
    @staticmethod
    def validate_return(requested: float, sold: float, already_returned: float) -> Tuple[bool, str]:
        if requested <= 0:
            return False, "Return quantity must be greater than 0"
        available_for_return = sold - already_returned
        if requested > available_for_return:
            return False, f"Cannot return {requested}. Only {available_for_return} available for return"
        return True, ""
