import sqlite3
import datetime as dt
from typing import List, Tuple
from .models import Product
from .interfaces import ProductRepository, SaleRepository

class SQLiteProductRepository(ProductRepository):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
    
    def get_all(self) -> List[Product]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_product, name_of_product, price, id_category, quantity_at_storage FROM producrs")
        return [Product(id=r[0], name=r[1], price=r[2], category_id=r[3], quantity_at_storage=r[4]) for r in cursor.fetchall()]
    
    def update_quantity(self, product_id: int, new_quantity: float) -> None:
        cursor = self.conn.cursor()
        cursor.execute("UPDATE producrs SET quantity_at_storage = ? WHERE id_product = ?", (new_quantity, product_id))
        self.conn.commit()

class SQLiteSaleRepository(SaleRepository):
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
    
    def create_receipt(self, cashier_id: int, items: List[Tuple[int, float]]) -> int:
        now_str = dt.datetime.now().isoformat()
        now_ts = dt.datetime.now().timestamp()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO reseipts (created_at, date, id_cashier) VALUES (?, ?, ?)", (now_ts, now_str, cashier_id))
        check_id = cursor.lastrowid
        for product_id, quantity in items:
            cursor.execute("INSERT INTO sale_items (id_check, id_product, quantity, date) VALUES (?, ?, ?, ?)", (check_id, product_id, quantity, now_str))
        self.conn.commit()
        return check_id
