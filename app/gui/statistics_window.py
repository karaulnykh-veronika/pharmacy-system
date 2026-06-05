"""Окно статистики продаж"""

import tkinter as tk
from tkinter import ttk


class StatisticsWindow:
    def __init__(self, parent, main_window):
        self.main = main_window
        self.window = tk.Toplevel(parent)
        self.window.geometry("600x500")
        self.window.title("Статистика продаж")
        self.window.configure(bg="#f0f0f0")
        self.window.protocol("WM_DELETE_WINDOW", self.close)
        
        self._create_widgets()
    
    def _create_widgets(self):
        main_frame = tk.Frame(self.window, bg="#f0f0f0", padx=15, pady=15)
        main_frame.pack(fill='both', expand=True)
        
        tk.Label(main_frame, text="📊 Статистика продаж", font="Arial 18 bold", bg="#f0f0f0", fg="#2c6e9e").pack(pady=10)
        
        # Период
        period_frame = tk.Frame(main_frame, bg="#f0f0f0")
        period_frame.pack(fill='x', pady=10)
        
        tk.Label(period_frame, text="Период (ГГГГ, ГГГГ-ММ или ГГГГ-ММ-ДД):", 
                font="Arial 12", bg="#f0f0f0", fg="#333333").pack(anchor='w')
        
        input_frame = tk.Frame(period_frame, bg="#f0f0f0")
        input_frame.pack(fill='x', pady=5)
        
        self.period_entry = tk.Entry(input_frame, font="Arial 12", width=25, relief="solid", bd=1)
        self.period_entry.pack(side='left', padx=(0,10))
        
        self.show_btn = tk.Button(input_frame, text="Показать", font="Arial 12", bg="#2c6e9e", 
                                 fg="white", relief="raised", command=self.show_stats)
        self.show_btn.pack(side='left')
        
        # Результаты
        self.result_text = tk.Text(main_frame, font="Arial 11", bg="#f8f8f8", fg="#333333",
                                   relief="solid", bd=1, height=15, wrap='word')
        self.result_text.pack(fill='both', expand=True, pady=10)
        
        # Скролл для результатов
        scrollbar = tk.Scrollbar(self.result_text)
        scrollbar.pack(side='right', fill='y')
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)
    
    def show_stats(self):
        period = self.period_entry.get().strip()
        if not period:
            self._show_error("Введите период")
            return
        
        # Определяем тип периода
        if len(period) == 4 and period.isdigit():
            where_clause = "si.date LIKE ?"
            param = period + '%'
            period_desc = f"год {period}"
        elif len(period) == 7 and period[4] == '-':
            year, month = period.split('-')
            if year.isdigit() and month.isdigit() and 1 <= int(month) <= 12:
                where_clause = "si.date LIKE ?"
                param = period + '%'
                period_desc = f"{year} год, месяц {month}"
            else:
                self._show_error("Неверный формат месяца")
                return
        elif len(period) == 10 and period[4] == '-' and period[7] == '-':
            where_clause = "DATE(si.date) = ?"
            param = period
            period_desc = f"день {period}"
        else:
            self._show_error("Введите ГГГГ, ГГГГ-ММ или ГГГГ-ММ-ДД")
            return
        
        cursor = self.main.conn.cursor()
        
        # Самый продаваемый товар
        cursor.execute(f"""
            SELECT p.name_of_product, SUM(si.quantity) as total_sold
            FROM sale_items si
            JOIN producrs p ON si.id_product = p.id_product
            WHERE {where_clause}
            GROUP BY si.id_product
            ORDER BY total_sold DESC
            LIMIT 1
        """, (param,))
        best = cursor.fetchone()
        
        # Топ-5 товаров
        cursor.execute(f"""
            SELECT p.name_of_product, SUM(si.quantity) as total_sold
            FROM sale_items si
            JOIN producrs p ON si.id_product = p.id_product
            WHERE {where_clause}
            GROUP BY si.id_product
            ORDER BY total_sold DESC
            LIMIT 5
        """, (param,))
        top5 = cursor.fetchall()
        
        # Общая выручка
        cursor.execute(f"""
            SELECT SUM(si.quantity * p.price) as total_revenue
            FROM sale_items si
            JOIN producrs p ON si.id_product = p.id_product
            WHERE {where_clause}
        """, (param,))
        revenue = cursor.fetchone()[0] or 0.0
        
        # Формируем вывод
        lines = []
        lines.append(f"📈 СТАТИСТИКА ЗА {period_desc.upper()}")
        lines.append("=" * 50)
        lines.append("")
        
        if best:
            lines.append(f"🏆 САМЫЙ ПРОДАВАЕМЫЙ ТОВАР:")
            lines.append(f"   {best[0]} — {best[1]:.0f} шт.")
        else:
            lines.append("❌ За этот период продаж не найдено.")
        
        lines.append("")
        lines.append(f"💰 ОБЩАЯ ВЫРУЧКА: {revenue:.2f} руб.")
        
        if top5 and len(top5) > 1:
            lines.append("")
            lines.append("📊 ТОП-5 ТОВАРОВ:")
            for i, (name, qty) in enumerate(top5, 1):
                lines.append(f"   {i}. {name} — {qty:.0f} шт.")
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, "\n".join(lines))
    
    def _show_error(self, message):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, f"❌ {message}")
    
    def close(self):
        self.window.destroy()
        self.main.statistics_window = None
    
    def winfo_exists(self):
        return self.window.winfo_exists()
    
    def lift(self):
        self.window.lift()
