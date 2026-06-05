"""Окно возврата товара"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime as dt


class ReturnWindow:
    def __init__(self, parent, main_window):
        self.main = main_window
        self.products_data = {}
        self.current_check_id = None
        
        self.window = tk.Toplevel(parent)
        self.window.geometry("650x650")
        self.window.title("Возврат товара")
        self.window.configure(bg="#f0f0f0")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self._create_widgets()
    
    def _create_widgets(self):
        main_frame = tk.Frame(self.window, bg="#f0f0f0", padx=15, pady=15)
        main_frame.pack(fill='both', expand=True)
        
        tk.Label(main_frame, text="Номер чека:", font="Arial 12", bg="#f0f0f0", fg="#333333").pack(anchor='w', pady=(0,5))
        
        check_frame = tk.Frame(main_frame, bg="#f0f0f0")
        check_frame.pack(anchor='w', fill='x', pady=(0,10))
        
        self.check_entry = tk.Entry(check_frame, font="Arial 12", width=20, relief="solid", bd=1)
        self.check_entry.pack(side='left', padx=(0,10))
        
        self.load_btn = tk.Button(check_frame, text="📋 Загрузить чек", font="Arial 11", bg="#e0e0e0", 
                                  relief="raised", command=self.load_check)
        self.load_btn.pack(side='left')
        
        self.status = tk.Label(main_frame, text="", font="Arial 12", bg="#f0f0f0")
        self.status.pack(pady=5)
        
        tk.Label(main_frame, text="Товары по чеку:", font="Arial 12", bg="#f0f0f0", fg="#333333").pack(anchor='w', pady=(10,5))
        
        # Список товаров с прокруткой
        list_frame = tk.Frame(main_frame, bg="#f0f0f0")
        list_frame.pack(fill='both', expand=True, pady=(0,10))
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.listbox = tk.Listbox(list_frame, font="Arial 11", height=8, bg="white", fg="#333333", 
                                  relief="solid", bd=1, yscrollcommand=scrollbar.set)
        self.listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Форма возврата
        return_frame = tk.Frame(main_frame, bg="#f0f0f0")
        return_frame.pack(fill='x', pady=10)
        
        tk.Label(return_frame, text="Количество для возврата:", font="Arial 12", bg="#f0f0f0", fg="#333333").pack(anchor='w', pady=(0,5))
        self.qty_entry = tk.Entry(return_frame, font="Arial 12", width=10, relief="solid", bd=1)
        self.qty_entry.pack(anchor='w', pady=(0,10))
        
        tk.Label(return_frame, text="Причина возврата:", font="Arial 12", bg="#f0f0f0", fg="#333333").pack(anchor='w', pady=(0,5))
        self.reason_var = tk.StringVar()
        reasons = ["Не подошёл", "Брак", "Передумал", "Истёк срок годности", "Другое"]
        self.reason_menu = ttk.Combobox(return_frame, textvariable=self.reason_var, values=reasons, 
                                        state="readonly", font="Arial 11")
        self.reason_menu.pack(anchor='w', pady=(0,10))
        self.reason_var.set(reasons[0])
        
        self.return_btn = tk.Button(return_frame, text="↩️ Вернуть товар", font="Arial 12", bg="#2c6e9e", 
                                   fg="white", relief="raised", padx=10, pady=5, 
                                   command=self.do_return, state='disabled')
        self.return_btn.pack(pady=10)
    
    def load_check(self):
        check_id_str = self.check_entry.get().strip()
        if not check_id_str.isdigit():
            self.status.config(text="❌ Введите корректный номер чека", fg="red")
            return
        
        self.current_check_id = int(check_id_str)
        
        # Проверяем существование чека
        cursor = self.main.conn.cursor()
        cursor.execute("SELECT id_check FROM reseipts WHERE id_check = ?", (self.current_check_id,))
        if not cursor.fetchone():
            self.status.config(text=f"❌ Чек №{self.current_check_id} не найден", fg="red")
            self.listbox.delete(0, tk.END)
            self.products_data.clear()
            self.return_btn.config(state='disabled')
            return
        
        # Загружаем товары из чека
        cursor.execute("""
            SELECT si.id_sale, p.name_of_product, si.quantity,
                   COALESCE(SUM(r.quantity_returned), 0) as returned,
                   p.price
            FROM sale_items si
            JOIN producrs p ON si.id_product = p.id_product
            LEFT JOIN returns r ON si.id_sale = r.id_sale
            WHERE si.id_check = ?
            GROUP BY si.id_sale
        """, (self.current_check_id,))
        items = cursor.fetchall()
        
        if not items:
            self.status.config(text="❌ В чеке нет товаров", fg="red")
            return
        
        self.listbox.delete(0, tk.END)
        self.products_data.clear()
        valid = False
        
        for sale_id, name, qty_sold, returned, price in items:
            available = qty_sold - returned
            if available > 0:
                display = f"{name} | Куплено: {qty_sold} | Доступно: {available} шт. | Цена: {price:.2f} руб."
                self.listbox.insert(tk.END, display)
                self.products_data[display] = (sale_id, name, available, price)
                valid = True
        
        if not valid:
            self.status.config(text="⚠️ Все товары из этого чека уже возвращены", fg="orange")
            self.return_btn.config(state='disabled')
        else:
            self.status.config(text=f"✅ Найдено {len(self.products_data)} позиций. Выберите товар.", fg="green")
            self.return_btn.config(state='normal')
    
    def do_return(self):
        selection = self.listbox.curselection()
        if not selection:
            self.status.config(text="❌ Выберите товар из списка", fg="red")
            return
        
        selected_text = self.listbox.get(selection[0])
        if selected_text not in self.products_data:
            self.status.config(text="❌ Ошибка: товар не найден", fg="red")
            return
        
        sale_id, product_name, max_available, price = self.products_data[selected_text]
        
        qty_str = self.qty_entry.get().strip()
        if not qty_str:
            self.status.config(text="❌ Введите количество", fg="red")
            return
        
        try:
            qty = float(qty_str)
        except ValueError:
            self.status.config(text="❌ Количество должно быть числом", fg="red")
            return
        
        if qty <= 0 or qty > max_available:
            self.status.config(text=f"❌ Можно вернуть от 1 до {max_available} шт.", fg="red")
            return
        
        reason = self.reason_var.get()
        now_ts = dt.datetime.now().timestamp()
        now_str = dt.datetime.now().isoformat()
        
        cursor = self.main.conn.cursor()
        try:
            # Записываем возврат
            cursor.execute("""
                INSERT INTO returns (id_sale, return_date, date, quantity_returned, reason) 
                VALUES (?, ?, ?, ?, ?)
            """, (sale_id, now_ts, now_str, qty, reason))
            
            # Возвращаем товар на склад
            cursor.execute("""
                UPDATE producrs 
                SET quantity_at_storage = quantity_at_storage + ? 
                WHERE id_product = (SELECT id_product FROM sale_items WHERE id_sale = ?)
            """, (qty, sale_id))
            
            self.main.conn.commit()
            
            # Обновляем кэш товаров
            self.main.products = self.main.product_repo.get_all()
            
            self.status.config(text=f"✅ Успешно возвращено {qty} шт. '{product_name}'", fg="green")
            
            # Очищаем поле и обновляем список
            self.qty_entry.delete(0, tk.END)
            self.load_check()
            
        except Exception as e:
            self.main.conn.rollback()
            self.status.config(text=f"❌ Ошибка: {e}", fg="red")
    
    def close(self):
        self.window.destroy()
        self.main.return_window = None
    
    def winfo_exists(self):
        return self.window.winfo_exists()
    
    def lift(self):
        self.window.lift()
