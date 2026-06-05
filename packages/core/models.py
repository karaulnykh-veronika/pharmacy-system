from dataclasses import dataclass

@dataclass
class Product:
    id: int
    name: str
    price: float
    category_id: int
    quantity_at_storage: float

@dataclass
class BasketItem:
    product_id: int
    product_name: str
    quantity: float
    price_per_unit: float
    
    @property
    def total_price(self) -> float:
        return self.quantity * self.price_per_unit
