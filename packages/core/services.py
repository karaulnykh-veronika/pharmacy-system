from typing import List, Optional
from .models import Product, BasketItem

def validate_quantity(quantity: float) -> None:
    if quantity <= 0:
        raise ValueError("Количество должно быть больше 0")

def calculate_item_total(price: float, quantity: float) -> float:
    if price < 0:
        raise ValueError("Цена не может быть отрицательной")
    if quantity <= 0:
        raise ValueError("Количество должно быть больше 0")
    return price * quantity

def check_stock_availability(product: Product, requested_quantity: float) -> bool:
    return product.quantity_at_storage >= requested_quantity

def find_product_by_name(products: List[Product], name: str) -> Optional[Product]:
    name_lower = name.strip().lower()
    for product in products:
        if product.name.lower() == name_lower:
            return product
    return None
