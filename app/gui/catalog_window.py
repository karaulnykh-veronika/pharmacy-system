"""Окно каталога товаров"""

import tkinter as tk


class CatalogWindow:
    def __init__(self, parent, products):
        self.products = products
        self.window = tk.Toplevel(parent)
        self.window.geometry("550x650")
        self.window.title("Каталог лекарств")
        self.window.configure(bg="#f0f0f0")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self._create_widgets()
        self._show_products()
    
    def _create_widgets(self):
        frame = tk.Frame(self.window, bg="#f0f0f0", padx=15, pady=15)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="📋 КАТАЛОГ ЛЕКАРСТВ", font="Arial 18 bold", bg="#f0f0f0", fg="#2c6e9e").pack(pady=10)
        
        # Поиск
        search_frame = tk.Frame(frame, bg="#f0f0f0")
        search_frame.pack(fill='x', pady=10)
        
        tk.Label(search_frame, text="🔍 Поиск:", font="Arial 12", bg="#f0f0f0").pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_frame, font="Arial 12", width=30, relief="solid", bd=1)
        self.search_entry.pack(side='left', fill='x', expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", self._filter)
        
        # Список товаров
        self.products_frame = tk.Frame(frame, bg="#f0f0f0")
        self.products_frame.pack(fill='both', expand=True, pady=10)
        
        # Прокрутка
        canvas = tk.Canvas(self.products_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.products_frame, orient="vertical", command=canvas.yview)
        self.scrollable = tk.Frame(canvas, bg="#f0f0f0")
        
        self.scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.scrollable_frame = self.scrollable
    
    def _show_products(self, filter_text=""):
        for w in self.scrollable_frame.winfo_children():
            w.destroy()
        
        filtered = self.products
        if filter_text:
            filtered = [p for p in filtered if filter_text.lower() in p.name.lower()]
        
        if not filtered:
            tk.Label(self.scrollable_frame, text="❌ Товары не найдены", font="Arial 14", 
                    bg="#f0f0f0", fg="red").pack(pady=30)
            return
        
        for p in filtered:
            text = f"💊 {p.name} — {p.price:.2f} руб. (остаток: {p.quantity_at_storage:.0f} шт.)"
            tk.Label(self.scrollable_frame, text=text, font="Arial 12", 
                    bg="#f0f0f0", fg="#333333", anchor='w').pack(fill='x', pady=3, padx=10)
    
    def _filter(self, event):
        self._show_products(self.search_entry.get().strip())
    
    def close(self):
        self.window.destroy()
    
    def winfo_exists(self):
        return self.window.winfo_exists()
    
    def lift(self):
        self.window.lift()
