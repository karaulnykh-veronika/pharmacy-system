"""Domain models for pharmacy system."""

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional
from enum import Enum


class ProductCategory(Enum):
    """Product categories in the pharmacy."""
    ANTIBIOTICS = 1
    PAIN_RELIEF = 2
    VITAMINS = 3
    CARDIOVASCULAR = 4
    ANTIVIRAL = 5
    
    @classmethod
    def from_id(cls, category_id: int) -> 'ProductCategory':
        for cat in cls:
            if cat.value == category_id:
                return cat
        raise ValueError(f"Unknown category id: {category_id}")
    
    @property
    def display_name(self) -> str:
        names = {
            ProductCategory.ANTIBIOTICS: "Антибиотики",
            ProductCategory.PAIN_RELIEF: "Обезболивающие",
            ProductCategory.VITAMINS: "Витамины",
            ProductCategory.CARDIOVASCULAR: "Сердечно-сосудистые",
            ProductCategory.ANTIVIRAL: "Противовирусные"
        }
        return names[self]


@dataclass
class Product:
    """Pharmacy product/medicine."""
    id: int
    name: str
    price: Decimal
    category_id: int
    quantity_in_stock: float
    
    @property
    def category(self) -> ProductCategory:
        return ProductCategory.from_id(self.category_id)
    
    @property
    def total_value(self) -> Decimal:
        return self.price * Decimal(str(self.quantity_in_stock))


@dataclass
class CartItem:
    """Item in shopping cart."""
    product_id: int
    product_name: str
    quantity: float
    price: Decimal
    
    @property
    def total(self) -> Decimal:
        return self.price * Decimal(str(self.quantity))


@dataclass
class ShoppingCart:
    """Shopping cart containing multiple items."""
    items: List[CartItem] = field(default_factory=list)
    
    def add_item(self, item: CartItem) -> None:
        for existing in self.items:
            if existing.product_id == item.product_id:
                existing.quantity += item.quantity
                return
        self.items.append(item)
    
    def remove_item(self, product_id: int) -> None:
        self.items = [i for i in self.items if i.product_id != product_id]
    
    @property
    def total(self) -> Decimal:
        return sum((item.total for item in self.items), Decimal(0))
    
    @property
    def item_count(self) -> int:
        return len(self.items)
    
    def clear(self) -> None:
        self.items.clear()
