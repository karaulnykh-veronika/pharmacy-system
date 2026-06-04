"""Database layer for pharmacy system."""

import csv
import sqlite3
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Tuple

from src.pharmacy.models import Product


class PharmacyDatabase:
    """Database manager for pharmacy system."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self) -> None:
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.cursor = self.conn.cursor()
    
    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.close()
    
    def init_tables(self) -> None:
        """Create all tables if they don't exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_titles (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                job_title_id INTEGER NOT NULL,
                FOREIGN KEY (job_title_id) REFERENCES job_titles(id)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                category_id INTEGER NOT NULL,
                quantity_in_stock REAL NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                date TEXT NOT NULL,
                cashier_id INTEGER NOT NULL,
                FOREIGN KEY (cashier_id) REFERENCES employees(id)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sale_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                receipt_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (receipt_id) REFERENCES receipts(id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS returns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sale_item_id INTEGER NOT NULL,
                return_timestamp REAL NOT NULL,
                date TEXT NOT NULL,
                quantity REAL NOT NULL,
                reason TEXT,
                FOREIGN KEY (sale_item_id) REFERENCES sale_items(id)
            )
        """)
        
        self.conn.commit()
    
    def load_csv_data(self, data_dir: Path) -> None:
        """Load initial data from CSV files if tables are empty."""
        
        self.cursor.execute("SELECT COUNT(*) FROM categories")
        if self.cursor.fetchone()[0] == 0:
            self._load_csv(data_dir / "categories.csv", "categories", ["id", "name"])
        
        self.cursor.execute("SELECT COUNT(*) FROM job_titles")
        if self.cursor.fetchone()[0] == 0:
            self._load_csv(data_dir / "job_titles.csv", "job_titles", ["id", "name"])
        
        self.cursor.execute("SELECT COUNT(*) FROM employees")
        if self.cursor.fetchone()[0] == 0:
            self._load_csv(data_dir / "employees.csv", "employees", ["id", "name", "surname", "job_title_id"])
        
        self.cursor.execute("SELECT COUNT(*) FROM products")
        if self.cursor.fetchone()[0] == 0:
            self._load_csv(data_dir / "products.csv", "products", 
                          ["id", "name", "price", "category_id", "quantity_in_stock"])
        
        self.conn.commit()
    
    def _load_csv(self, filepath: Path, table: str, columns: List[str]) -> None:
        if not filepath.exists():
            return
        
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                placeholders = ','.join(['?'] * len(row))
                self.cursor.execute(
                    f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})",
                    row
                )
    
    def get_all_products(self) -> List[Product]:
        self.cursor.execute("""
            SELECT id, name, price, category_id, quantity_in_stock 
            FROM products
        """)
        return [
            Product(id=row[0], name=row[1], price=Decimal(str(row[2])),
                   category_id=row[3], quantity_in_stock=row[4])
            for row in self.cursor.fetchall()
        ]
    
    def update_product_stock(self, product_id: int, new_quantity: float) -> None:
        self.cursor.execute(
            "UPDATE products SET quantity_in_stock = ? WHERE id = ?",
            (new_quantity, product_id)
        )
        self.conn.commit()
    
    def create_receipt(self, timestamp: float, date_str: str, cashier_id: int) -> int:
        self.cursor.execute(
            "INSERT INTO receipts (timestamp, date, cashier_id) VALUES (?, ?, ?)",
            (timestamp, date_str, cashier_id)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def add_sale_item(self, receipt_id: int, product_id: int, quantity: float, date_str: str) -> None:
        self.cursor.execute(
            "INSERT INTO sale_items (receipt_id, product_id, quantity, date) VALUES (?, ?, ?, ?)",
            (receipt_id, product_id, quantity, date_str)
        )
        self.conn.commit()
    
    def get_receipt_exists(self, receipt_id: int) -> bool:
        self.cursor.execute("SELECT 1 FROM receipts WHERE id = ?", (receipt_id,))
        return self.cursor.fetchone() is not None
