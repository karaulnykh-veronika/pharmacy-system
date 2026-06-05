"""Окно добавления товаров на склад"""

import tkinter as tk


class StorageWindow:
    def __init__(self, parent, main_window):
        self.main = main_window
        self.window = tk.Toplevel(parent)
        self.window.geometry("550x300")
        self.window.title("Склад - добавление товаров")
        self.window.configure(bg="#f0f0f0")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self._create_widgets()
    
    def _create_widgets(self):
        frame = tk.Frame(self.window, bg="#f0f0f0", padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        input_frame = tk.Frame(frame, bg="#f0f0f0")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Название товара:", font="Arial 12", bg="#f0f0f0", fg="#333333").pack(side='left', padx=(0,5))
        self.name_entry = tk.Entry(input_frame, font="Arial 12", width=20, relief="solid", bd=1)
        self.name_entry.pack(side='left', padx=(0,15))
        
        tk.Label(input_frame, text="Количество:", font="Arial 12", bg="#f0f0f0", fg="#333333").pack(side='left', padx=(0,5))
        self.qty_entry = tk.Entry(input_frame, font="Arial 12", width=8, relief="solid", bd=1)
        self.qty_entry.pack(side='left')
        
        self.status = tk.Label(frame, text="", font="Arial 12", bg="#f0f0f0")
        self.status.pack(pady=10)
        
        btn = tk.Button(frame, text="➕ Добавить на склад", font="Arial 12", bg="#2c6e9e", fg="white",
                       relief="raised", padx=10, pady=5, command=self.add_to_storage)
        btn.pack(pady=10)
    
    def add_to_storage(self):
        name = self.name_entry.get().strip()
        try:
            count = float(self.qty_entry.get())
            if count <= 0:
                raise ValueError("Количество должно быть больше 0")
        except ValueError as e:
            self.status.config(text=str(e), fg="red")
            return
        
        # Ищем товар
        for product in self.main.products:
            if product.name.lower() == name.lower():
                new_qty = product.quantity_at_storage + count
                self.main.product_repo.update_quantity(product.id, new_qty)
                product.quantity_at_storage = new_qty
                self.status.config(text=f"✅ {product.name}: +{count} шт. (Всего: {new_qty})", fg="green")
                self.name_entry.delete(0, tk.END)
                self.qty_entry.delete(0, tk.END)
                return
        
        self.status.config(text="❌ Такого товара нет в каталоге!", fg="red")
    
    def close(self):
        self.window.destroy()
        self.main.storage_window = None
    
    def winfo_exists(self):
        return self.window.winfo_exists()
    
    def lift(self):
        self.window.lift()
