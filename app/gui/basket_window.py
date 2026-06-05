"""Окно корзины"""

import tkinter as tk
from tkinter import messagebox
import datetime as dt


class BasketWindow:
    def __init__(self, parent, main_window):
        self.main = main_window
        self.window = tk.Toplevel(parent)
        self.window.geometry("550x600")
        self.window.title("Корзина")
        self.window.configure(bg="#f0f0f0")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self._create_widgets()
        self.refresh()
    
    def _create_widgets(self):
        frame = tk.Frame(self.window, bg="#f0f0f0", padx=15, pady=15)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="🛒 КОРЗИНА", font="Arial 18 bold", bg="#f0f0f0", fg="#2c6e9e").pack()
        
        # Список товаров
        items_frame = tk.Frame(frame, bg="#f0f0f0")
        items_frame.pack(fill='both', expand=True, pady=10)
        
        canvas = tk.Canvas(items_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = tk.Scrollbar(items_frame, orient="vertical", command=canvas.yview)
        self.scrollable = tk.Frame(canvas, bg="#f0f0f0")
        
        self.scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Нижняя панель
        bottom = tk.Frame(frame, bg="#f0f0f0")
        bottom.pack(fill='x', pady=10)
        
        self.total_lbl = tk.Label(bottom, text="", font="Arial 16 bold", bg="#f0f0f0", fg="#2c6e9e")
        self.total_lbl.pack(side='left', padx=10)
        
        btn_buy = tk.Button(bottom, text="✅ КУПИТЬ", font="Arial 14", bg="#2c6e9e", fg="white",
                           relief="raised", padx=15, pady=5, command=self.buy)
        btn_buy.pack(side='right', padx=10)
    
    def refresh(self):
        for w in self.scrollable.winfo_children():
            w.destroy()
        
        self.total_lbl.config(text=f"💰 ИТОГО: {self.main.all_sum:.2f} руб.")
        
        if not self.main.basket:
            tk.Label(self.scrollable, text="Корзина пуста", font="Arial 14", 
                    bg="#f0f0f0", fg="#888888").pack(pady=20)
            return
        
        for item in self.main.basket:
            item_frame = tk.Frame(self.scrollable, bg="#f0f0f0")
            item_frame.pack(fill='x', pady=5)
            
            text = f"{item.product_name} x {item.quantity} = {item.total_price:.2f} руб."
            lbl = tk.Label(item_frame, text=text, font="Arial 12", fg="#333333", bg="#f0f0f0")
            lbl.pack(side='left')
    
    def buy(self):
        if not self.main.basket:
            return
        
        items = [(item.product_id, item.quantity) for item in self.main.basket]
        check_id = self.main.sale_repo.create_receipt(cashier_id=1, items=items)
        
        self._show_receipt(check_id)
        
        self.main.basket = []
        self.main.all_sum = 0.0
        self.refresh()
    
    def _show_receipt(self, check_id):
        """Показывает красивый чек"""
        receipt_win = tk.Toplevel(self.window)
        receipt_win.title(f"🧾 ЧЕК №{check_id}")
        receipt_win.geometry("500x600")
        receipt_win.configure(bg="#f0f0f0")
        
        frame = tk.Frame(receipt_win, bg="white", padx=20, pady=20, relief="solid", bd=1)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Шапка
        tk.Label(frame, text="🏥 АПТЕКА", font="Arial 18 bold", bg="white", fg="#2c6e9e").pack(pady=5)
        tk.Label(frame, text=f"ЧЕК №{check_id}", font="Arial 14 bold", bg="white", fg="#333333").pack()
        
        now_str = dt.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        tk.Label(frame, text=now_str, font="Arial 10", bg="white", fg="#888888").pack(pady=5)
        
        tk.Label(frame, text="─" * 40, font="Arial 10", bg="white", fg="#cccccc").pack(pady=5)
        
        # Таблица товаров
        headers_frame = tk.Frame(frame, bg="white")
        headers_frame.pack(fill='x')
        
        tk.Label(headers_frame, text="Товар", width=25, anchor='w', font="Arial 10 bold", bg="white").grid(row=0, column=0, sticky='w')
        tk.Label(headers_frame, text="Кол-во", width=6, anchor='e', font="Arial 10 bold", bg="white").grid(row=0, column=1, padx=5)
        tk.Label(headers_frame, text="Цена", width=8, anchor='e', font="Arial 10 bold", bg="white").grid(row=0, column=2, padx=5)
        tk.Label(headers_frame, text="Сумма", width=8, anchor='e', font="Arial 10 bold", bg="white").grid(row=0, column=3, padx=5)
        
        for i, item in enumerate(self.main.basket, start=1):
            tk.Label(frame, text=item.product_name[:25], width=25, anchor='w', font="Arial 10", bg="white").grid(row=i+1, column=0, sticky='w', padx=(0,0))
            tk.Label(frame, text=str(int(item.quantity)) if item.quantity.is_integer() else str(item.quantity), 
                    width=6, anchor='e', font="Arial 10", bg="white").grid(row=i+1, column=1, padx=5)
            tk.Label(frame, text=f"{item.price_per_unit:.2f}", width=8, anchor='e', font="Arial 10", bg="white").grid(row=i+1, column=2, padx=5)
            tk.Label(frame, text=f"{item.total_price:.2f}", width=8, anchor='e', font="Arial 10", bg="white").grid(row=i+1, column=3, padx=5)
        
        # Итого
        tk.Label(frame, text="─" * 40, font="Arial 10", bg="white", fg="#cccccc").pack(pady=5)
        tk.Label(frame, text=f"ИТОГО: {self.main.all_sum:.2f} руб.", font="Arial 14 bold", 
                bg="white", fg="#2c6e9e").pack(pady=5)
        tk.Label(frame, text="Спасибо за покупку! 💊", font="Arial 10", bg="white", fg="#888888").pack()
        
        tk.Button(frame, text="Закрыть", font="Arial 12", bg="#2c6e9e", fg="white",
                 relief="raised", command=receipt_win.destroy).pack(pady=15)
        
        # Центрируем окно
        receipt_win.update_idletasks()
        x = (receipt_win.winfo_screenwidth() // 2) - (receipt_win.winfo_width() // 2)
        y = (receipt_win.winfo_screenheight() // 2) - (receipt_win.winfo_height() // 2)
        receipt_win.geometry(f"+{x}+{y}")
    
    def close(self):
        self.window.destroy()
        self.main.basket_window = None
    
    def winfo_exists(self):
        return self.window.winfo_exists()
    
    def lift(self):
        self.window.lift()
