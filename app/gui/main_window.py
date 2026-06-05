"""Главное окно аптеки"""

import tkinter as tk
from tkinter import messagebox
import datetime as dt
import os
import sqlite3

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from packages.core.models import BasketItem
from packages.core.services import (
    validate_quantity, check_stock_availability,
    find_product_by_name
)
from packages.core.repositories import (
    SQLiteProductRepository, SQLiteSaleRepository
)


def get_database_path():
    return os.path.join(os.path.dirname(__file__), "..", "..", "pharmacy.db")


class MainWindow:
    def __init__(self):
        db_path = get_database_path()
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        
        self._init_database()
        
        self.product_repo = SQLiteProductRepository(self.conn)
        self.sale_repo = SQLiteSaleRepository(self.conn)
        
        self.products = self.product_repo.get_all()
        
        self.basket = []
        self.all_sum = 0.0
        
        # Окна
        self.basket_window = None
        self.catalog_window = None
        self.storage_window = None
        self.return_window = None
        self.statistics_window = None
        
        self.root = tk.Tk()
        self.root.geometry("970x400")
        self.root.title("Аптека - Система управления")
        self.root.configure(bg="#f0f0f0")
        
        self._create_widgets()
    
    def _init_database(self):
        cursor = self.conn.cursor()
        
        # Таблица должностей
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs_titles (
                id_job_title INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)
        
        # Таблица сотрудников
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emploees (
                id_employee INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                id_job_title INTEGER NOT NULL,
                FOREIGN KEY(id_job_title) REFERENCES jobs_titles(id_job_title)
            )
        """)
        
        # Таблица категорий
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id_category INTEGER PRIMARY KEY,
                name_category TEXT NOT NULL
            )
        """)
        
        # Таблица товаров
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS producrs (
                id_product INTEGER PRIMARY KEY,
                name_of_product TEXT NOT NULL,
                price REAL NOT NULL,
                id_category INTEGER NOT NULL,
                quantity_at_storage REAL NOT NULL,
                FOREIGN KEY(id_category) REFERENCES categories(id_category)
            )
        """)
        
        # Таблица чеков
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reseipts (
                id_check INTEGER PRIMARY KEY,
                created_at REAL NOT NULL,
                date TEXT NOT NULL,
                id_cashier INTEGER NOT NULL,
                FOREIGN KEY(id_cashier) REFERENCES emploees(id_employee)
            )
        """)
        
        # Таблица позиций в чеках
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sale_items (
                id_sale INTEGER PRIMARY KEY,
                id_check INTEGER NOT NULL,
                id_product INTEGER NOT NULL,
                quantity REAL NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY(id_check) REFERENCES reseipts(id_check),
                FOREIGN KEY(id_product) REFERENCES producrs(id_product)
            )
        """)
        
        # Таблица возвратов
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS returns (
                id_return INTEGER PRIMARY KEY,
                id_sale INTEGER NOT NULL,
                return_date REAL NOT NULL,
                date TEXT NOT NULL,
                quantity_returned REAL NOT NULL,
                reason TEXT,
                FOREIGN KEY(id_sale) REFERENCES sale_items(id_sale)
            )
        """)
        
        self.conn.commit()
        
        # Добавляем категории, если их нет
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO categories (id_category, name_category) VALUES (1, 'Лекарства')")
            cursor.execute("INSERT INTO categories (id_category, name_category) VALUES (2, 'БАДы')")
            cursor.execute("INSERT INTO categories (id_category, name_category) VALUES (3, 'Медизделия')")
            self.conn.commit()
        
        # Добавляем должность, если нет
        cursor.execute("SELECT COUNT(*) FROM jobs_titles")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO jobs_titles (id_job_title, name) VALUES (1, 'Фармацевт')")
            self.conn.commit()
        
        # Добавляем сотрудника, если нет
        cursor.execute("SELECT COUNT(*) FROM emploees")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO emploees (id_employee, name, surname, id_job_title) VALUES (1, 'Admin', 'Admin', 1)")
            self.conn.commit()
        
        # Добавляем товары, если их нет
        cursor.execute("SELECT COUNT(*) FROM producrs")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO producrs (id_product, name_of_product, price, id_category, quantity_at_storage) VALUES (1, 'Аспирин', 50, 1, 100)")
            cursor.execute("INSERT INTO producrs (id_product, name_of_product, price, id_category, quantity_at_storage) VALUES (2, 'Парацетамол', 30, 1, 150)")
            cursor.execute("INSERT INTO producrs (id_product, name_of_product, price, id_category, quantity_at_storage) VALUES (3, 'Нурофен', 120, 1, 80)")
            cursor.execute("INSERT INTO producrs (id_product, name_of_product, price, id_category, quantity_at_storage) VALUES (4, 'Витамин C', 200, 2, 50)")
            cursor.execute("INSERT INTO producrs (id_product, name_of_product, price, id_category, quantity_at_storage) VALUES (5, 'Бинт', 25, 3, 200)")
            self.conn.commit()
        
        self.conn.commit()
    
    def _create_widgets(self):
        top_frame = tk.Frame(self.root, bg="#f0f0f0", padx=15, pady=15)
        top_frame.pack(fill='x')
        
        input_frame = tk.Frame(top_frame, bg="#f0f0f0")
        input_frame.pack(fill='x', pady=5)
        
        tk.Label(input_frame, text="Название лекарства:", font="Arial 14", bg="#f0f0f0").pack(side='left', padx=5)
        self.textfield = tk.Entry(input_frame, font="Arial 14", width=30, relief="solid", bd=1)
        self.textfield.pack(side='left', padx=5)
        
        tk.Label(input_frame, text="Кол-во:", font="Arial 14", bg="#f0f0f0").pack(side='left', padx=5)
        self.cnt = tk.Entry(input_frame, font="Arial 14", width=6, relief="solid", bd=1)
        self.cnt.pack(side='left', padx=5)
        
        self.qn = tk.Label(top_frame, text="", font="Arial 14", bg="#f0f0f0")
        self.qn.pack(pady=5)
        
        btn_add = tk.Button(top_frame, text="Добавить в корзину", font="Arial 14",
                           bg="#2c6e9e", fg="white", relief="raised",
                           padx=10, pady=5, command=self.add_to_cart)
        btn_add.pack(pady=5)
        
        bottom_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10, pady=10)
        bottom_frame.pack(side='bottom', fill='x')
        
        buttons = [
            ("📦 Добавить на склад", self.open_storage),
            ("↩️ Вернуть товар", self.open_return),
            ("🛒 Корзина", self.open_basket),
            ("📋 Каталог", self.open_catalog),
            ("📊 Статистика", self.open_statistics)
        ]
        
        for text, command in buttons:
            btn = tk.Button(bottom_frame, text=text, font="Arial 14", bg="#e0e0e0", 
                           relief="raised", padx=10, pady=5, command=command)
            btn.pack(side='left', padx=10, expand=True)
    
    def add_to_cart(self):
        name = self.textfield.get().strip()
        
        try:
            quantity = float(self.cnt.get())
            validate_quantity(quantity)
        except ValueError as e:
            self.qn.config(text=str(e), fg="red")
            return
        
        product = find_product_by_name(self.products, name)
        if not product:
            self.qn.config(text="Такого товара нет в каталоге!", fg="red")
            return
        
        if not check_stock_availability(product, quantity):
            self.qn.config(text=f"Недостаточно! Осталось: {product.quantity_at_storage}", fg="red")
            return
        
        new_quantity = product.quantity_at_storage - quantity
        self.product_repo.update_quantity(product.id, new_quantity)
        product.quantity_at_storage = new_quantity
        
        basket_item = BasketItem(
            product_id=product.id,
            product_name=product.name,
            quantity=quantity,
            price_per_unit=product.price
        )
        self.basket.append(basket_item)
        self.all_sum += basket_item.total_price
        
        self.qn.config(text=f"✓ {product.name} добавлен в корзину", fg="green")
        self.textfield.delete(0, tk.END)
        self.cnt.delete(0, tk.END)
    
    def open_basket(self):
        if self.basket_window and self.basket_window.winfo_exists():
            self.basket_window.lift()
            return
        from app.gui.basket_window import BasketWindow
        self.basket_window = BasketWindow(self.root, self)
    
    def open_catalog(self):
        if self.catalog_window and self.catalog_window.winfo_exists():
            self.catalog_window.lift()
            return
        from app.gui.catalog_window import CatalogWindow
        self.catalog_window = CatalogWindow(self.root, self.products)
    
    def open_storage(self):
        if self.storage_window and self.storage_window.winfo_exists():
            self.storage_window.lift()
            return
        from app.gui.storage_window import StorageWindow
        self.storage_window = StorageWindow(self.root, self)
    
    def open_return(self):
        if self.return_window and self.return_window.winfo_exists():
            self.return_window.lift()
            return
        from app.gui.return_window import ReturnWindow
        self.return_window = ReturnWindow(self.root, self)
    
    def open_statistics(self):
        if self.statistics_window and self.statistics_window.winfo_exists():
            self.statistics_window.lift()
            return
        from app.gui.statistics_window import StatisticsWindow
        self.statistics_window = StatisticsWindow(self.root, self)
    
    def clear_basket(self):
        self.basket = []
        self.all_sum = 0.0
    
    def run(self):
        self.root.mainloop()
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
