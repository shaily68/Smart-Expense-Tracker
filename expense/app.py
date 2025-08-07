from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

EXPENSES_FILE = 'expenses.csv'

@app.route('/')
def index():
    expenses = []
    total = 0.0
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                expenses.append(row)
                try:
                    total += float(row[2])  # Amount is at index 2
                except:
                    pass
    return render_template('index.html', expenses=expenses, total=total)

@app.route('/add', methods=['POST'])
def add_expense():
    date = request.form['date']
    category = request.form['category']
    amount = request.form['amount']
    description = request.form['description']

    with open(EXPENSES_FILE, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([date, category, amount, description])

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
