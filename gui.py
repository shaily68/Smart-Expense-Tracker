from matplotlib import pyplot as plt
from fpdf import FPDF
import csv
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from datetime import datetime
from tkinter import messagebox

FILENAME = "expenses.csv"

def show_pie_chart():
    try:
        categories = {}
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3:
                    category = row[1]
                    amount = float(row[2])
                    categories[category] = categories.get(category, 0) + amount

        if not categories:
            messagebox.showinfo("No Data", "No expense data to show.")
            return

        labels = list(categories.keys())
        values = list(categories.values())

        plt.figure(figsize=(6, 6))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Expense Distribution by Category")
        plt.axis('equal')
        plt.show()
    except Exception as e:
        messagebox.showerror("Chart Error", str(e))


def export_to_pdf():
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Expense Tracker Report", ln=True, align='C')
        pdf.ln(10)

        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 4:
                    line = f"Date: {row[0]}  |  Category: {row[1]}  |  Amount: {row[2]}  |  Desc: {row[3]}"
                    pdf.multi_cell(0, 10, txt=line)

        pdf.output("expense_report.pdf")
        messagebox.showinfo("Success", "PDF report saved as 'expense_report.pdf'!")
    except Exception as e:
        messagebox.showerror("PDF Error", str(e))

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()
    desc = desc_entry.get()

    if not date or not category or not amount:
        messagebox.showerror("❗Missing Info", "Please fill all fields!")
        return

    try:
        float(amount)
    except ValueError:
        messagebox.showerror("Invalid", "Amount must be a number!")
        return

    with open(FILENAME, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, desc])

    clear_fields()
    load_expenses()
    

def load_expenses():
    for row in tree.get_children():
        tree.delete(row)

    try:
        with open(FILENAME, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert('', END, values=row)
    except FileNotFoundError:
        open(FILENAME, 'w').close()

def clear_fields():
    date_entry.delete(0, END)
    category_entry.delete(0, END)
    amount_entry.delete(0, END)
    desc_entry.delete(0, END)

# -------- GUI Window --------
app = tb.Window(themename="cosmo")  # Vibrant theme
app.title("🌸 My Beautiful Expense Tracker")
app.geometry("750x600")
app.configure(bg="#fff0f5")  # light lavender-pink background

# -------- Title --------
title = tb.Label(app, text="🌈 Expense Tracker", font=("Comic Sans MS", 26, "bold"), background="#fff0f5", foreground="#800080")
title.pack(pady=20)

# -------- Input Frame --------
input_frame = tb.Frame(app, padding=20, bootstyle="light")
input_frame.pack(pady=10)

btn = tb.Button(app, text=" Add Expense", bootstyle="success outline",  compound=LEFT, command=add_expense)
btn.pack(pady=10)

# 🆕 New Buttons Below This
btn_chart = tb.Button(app, text="📊 Show Pie Chart", bootstyle="info outline", command=show_pie_chart)
btn_chart.pack(pady=5)

btn_pdf = tb.Button(app, text="📄 Export to PDF", bootstyle="warning outline", command=export_to_pdf)
btn_pdf.pack(pady=5)

def create_label(text, row):
    label = tb.Label(input_frame, text=text, font=("Segoe UI", 11, "bold"), foreground="#5c0066")
    label.grid(row=row, column=0, sticky="w", padx=5, pady=5)

def create_entry(row):
    entry = tb.Entry(input_frame, width=30, font=("Segoe UI", 10))
    entry.grid(row=row, column=1, padx=10, pady=5)
    return entry

create_label("📅 Date (YYYY-MM-DD):", 0)
date_entry = create_entry(0)
date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

create_label("👜 Category:", 1)
category_entry = create_entry(1)

create_label("💵 Amount:", 2)
amount_entry = create_entry(2)

create_label("📝 Description:", 3)
desc_entry = create_entry(3)

# -------- Button --------
btn = tb.Button(app, text="➕ Add Expense", bootstyle="success outline", width=20, command=add_expense)
btn.pack(pady=15)

# -------- Table --------
tree = tb.Treeview(app, columns=("Date", "Category", "Amount", "Description"), show="headings", height=10, bootstyle="info")
style = tb.Style()
style.configure("Treeview.Heading", font=("Calibri", 11, "bold"), foreground="#333")

for col in ("Date", "Category", "Amount", "Description"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)

tree.pack(fill="both", expand=True, padx=20, pady=10)

load_expenses()
app.mainloop()