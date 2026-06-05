from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from .models import Product

class ProductRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Product]:
        pass
    @abstractmethod
    def update_quantity(self, product_id: int, new_quantity: float) -> None:
        pass

class SaleRepository(ABC):
    @abstractmethod
    def create_receipt(self, cashier_id: int, items: List[Tuple[int, float]]) -> int:
        pass
