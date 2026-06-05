"""Главное окно аптеки"""

import tkinter as tk
from tkinter import messagebox
import datetime as dt
import os
import sqlite3

# Добавляем путь к packages в sys.path (для работы из любой папки)
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
    """Возвращает путь к файлу базы данных"""
    return os.path.join(os.path.dirname(__file__), "..", "..", "pharmacy.db")


class MainWindow:
    def __init__(self):
        # Подключаемся к БД
        db_path = get_database_path()
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        
        # Создаём таблицы, если их нет
        self._init_database()
        
        # Создаём репозитории
        self.product_repo = SQLiteProductRepository(self.conn)
        self.sale_repo = SQLiteSaleRepository(self.conn)
        
        # Загружаем товары
        self.products = self.product_repo.get_all()
        
        # Состояние корзины
        self.basket = []
        self.all_sum = 0.0
        
        # Создаём окно
        self.root = tk.Tk()
        self.root.geometry("970x400")
        self.root.title("Аптека - Система управления")
        self.root.configure(bg="#f0f0f0")
        
        self._create_widgets()
    
    def _init_database(self):
        """Создаёт таблицы, если их нет"""
        cursor = self.conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id_category INTEGER PRIMARY KEY,
                name_category TEXT NOT NULL
            )
        """)
        
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
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emploees (
                id_employee INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                id_job_title INTEGER NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reseipts (
                id_check INTEGER PRIMARY KEY,
                created_at REAL NOT NULL,
                date TEXT NOT NULL,
                id_cashier INTEGER NOT NULL,
                FOREIGN KEY(id_cashier) REFERENCES emploees(id_employee)
            )
        """)
        
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
        
        # Добавляем тестового сотрудника, если нет
        cursor.execute("SELECT COUNT(*) FROM emploees")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO emploees (id_employee, name, surname, id_job_title) VALUES (1, 'Admin', 'Admin', 1)")
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
        
        btn_basket = tk.Button(bottom_frame, text="Корзина", font="Arial 14",
                              bg="#e0e0e0", relief="raised",
                              padx=10, pady=5, command=self.open_basket)
        btn_basket.pack(side='left', padx=10, expand=True)
        
        btn_catalog = tk.Button(bottom_frame, text="Каталог", font="Arial 14",
                               bg="#e0e0e0", relief="raised",
                               padx=10, pady=5, command=self.open_catalog)
        btn_catalog.pack(side='left', padx=10, expand=True)
    
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
        if hasattr(self, 'basket_window') and self.basket_window and self.basket_window.winfo_exists():
            self.basket_window.lift()
            return
        self.basket_window = BasketWindow(self)
    
    def open_catalog(self):
        CatalogWindow(self)
    
    def run(self):
        self.root.mainloop()
    
    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


class BasketWindow:
    def __init__(self, main_window):
        self.main = main_window
        self.window = tk.Toplevel(main_window.root)
        self.window.geometry("500x550")
        self.window.title("Корзина")
        self.window.configure(bg="#f0f0f0")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self._create_widgets()
        self.refresh()
    
    def _create_widgets(self):
        frame = tk.Frame(self.window, bg="#f0f0f0", padx=15, pady=15)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="Корзина", font="Arial 18 bold", bg="#f0f0f0", fg="#2c6e9e").pack()
        
        items_frame = tk.Frame(frame, bg="#f0f0f0")
        items_frame.pack(fill='both', expand=True, pady=10)
        
        self.scrollable = tk.Frame(items_frame, bg="#f0f0f0")
        self.scrollable.pack(fill='both', expand=True)
        
        bottom = tk.Frame(frame, bg="#f0f0f0")
        bottom.pack(fill='x', pady=10)
        
        self.total_lbl = tk.Label(bottom, text="", font="Arial 16 bold", bg="#f0f0f0", fg="#2c6e9e")
        self.total_lbl.pack(side='left', padx=10)
        
        btn_buy = tk.Button(bottom, text="Купить", font="Arial 14", bg="#2c6e9e", fg="white",
                           relief="raised", padx=15, pady=5, command=self.buy)
        btn_buy.pack(side='right', padx=10)
    
    def refresh(self):
        for w in self.scrollable.winfo_children():
            w.destroy()
        
        self.total_lbl.config(text=f"Итоговая сумма: {self.main.all_sum:.2f} руб.")
        
        for item in self.main.basket:
            lbl = tk.Label(self.scrollable, text=f"{item.product_name} x {item.quantity} = {item.total_price:.2f} руб.",
                          font="Arial 12", fg="#2c6e9e", bg="#f0f0f0")
            lbl.pack(anchor='w', pady=2)
    
    def buy(self):
        if not self.main.basket:
            return
        
        items = [(item.product_id, item.quantity) for item in self.main.basket]
        check_id = self.main.sale_repo.create_receipt(cashier_id=1, items=items)
        
        messagebox.showinfo("Успех", f"Покупка оформлена!\nЧек №{check_id}\nСумма: {self.main.all_sum:.2f} руб.")
        
        self.main.basket = []
        self.main.all_sum = 0.0
        self.refresh()
        self.close()
    
    def close(self):
        self.window.destroy()
        self.main.basket_window = None
    
    def winfo_exists(self):
        return self.window.winfo_exists()
    
    def lift(self):
        self.window.lift()


class CatalogWindow:
    def __init__(self, main_window):
        self.main = main_window
        self.window = tk.Toplevel(main_window.root)
        self.window.geometry("500x650")
        self.window.title("Каталог лекарств")
        self.window.configure(bg="#f0f0f0")
        
        self._create_widgets()
        self._show_products()
    
    def _create_widgets(self):
        frame = tk.Frame(self.window, bg="#f0f0f0", padx=15, pady=15)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="Каталог лекарств", font="Arial 18 bold", bg="#f0f0f0", fg="#2c6e9e").pack(pady=10)
        
        search_frame = tk.Frame(frame, bg="#f0f0f0")
        search_frame.pack(fill='x', pady=5)
        
        self.search_entry = tk.Entry(search_frame, font="Arial 12", width=30, relief="solid", bd=1)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", self._filter)
        
        self.products_frame = tk.Frame(frame, bg="#f0f0f0")
        self.products_frame.pack(fill='both', expand=True, pady=10)
    
    def _show_products(self, filter_text=""):
        for w in self.products_frame.winfo_children():
            w.destroy()
        
        filtered = self.main.products
        if filter_text:
            filtered = [p for p in filtered if filter_text.lower() in p.name.lower()]
        
        for p in filtered:
            tk.Label(self.products_frame, text=f"{p.name} — {p.price:.2f} руб. (остаток: {p.quantity_at_storage})",
                    font="Arial 12", bg="#f0f0f0", fg="#333333").pack(anchor='w', pady=2, padx=10)
    
    def _filter(self, event):
        self._show_products(self.search_entry.get())


if __name__ == "__main__":
    app = MainWindow()
    app.run()
