from flask import Flask, request, redirect, url_for, render_template, session
from datetime import datetime, date
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from calendar import monthrange

app = Flask(__name__)
app.secret_key = 'my_super_secret_key'

def get_db_connection():
    conn = sqlite3.connect('my_budget.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            item TEXT NOT NULL,
            amount INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    hashed_password = generate_password_hash(password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def check_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        return user['id']
    return None

def add_transaction(user_id, date, item, amount):
    conn = get_db_connection()
    conn.execute("INSERT INTO transactions (user_id, date, item, amount) VALUES (?, ?, ?, ?)",
                 (user_id, date, item, amount))
    conn.commit()
    conn.close()

def get_transactions_by_user(user_id):
    conn = sqlite3.connect('my_budget.db')
    conn.row_factory = sqlite3.Row
    transactions = conn.execute("SELECT date, item, amount FROM transactions WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return transactions

def get_balance(user_id):
    conn = get_db_connection()
    balance_row = conn.execute("SELECT SUM(amount) AS total FROM transactions WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return balance_row['total'] if balance_row['total'] is not None else 0

@app.route('/')
def home():
    if 'user_id' not in session:
        return render_template('home.html')
    
    username = session.get('username')
    balance = get_balance(session['user_id'])
    
    return render_template(
        'index.html',
        username=username,
        balance=balance
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            return "<h1>회원가입 성공! 로그인 페이지로 이동하세요.</h1><a href='/login'>로그인</a>"
        else:
            return "<h1>이미 존재하는 아이디입니다.</h1><a href='/register'>다시 시도</a>"
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = check_user(username, password)
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "<h1>로그인 실패. 아이디 또는 비밀번호를 확인하세요.</h1>"
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        date = request.form['date']
        item = request.form['item']
        amount = int(request.form['amount'])
        transaction_type = request.form['transaction_type']
        
        if transaction_type == 'expense':
            amount = -amount

        add_transaction(session['user_id'], date, item, amount)
        return redirect(url_for('home'))
    
    return render_template('add.html')

@app.route('/view')
def view():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    year = int(request.args.get('year', date.today().year))
    month = int(request.args.get('month', date.today().month))

    conn = get_db_connection()
    transactions_raw = conn.execute("""
        SELECT date, item, amount
        FROM transactions
        WHERE user_id = ? AND SUBSTR(date, 1, 4) = ? AND SUBSTR(date, 6, 2) = ?
        ORDER BY date ASC
    """, (session['user_id'], str(year), f'{month:02d}')).fetchall()
    conn.close()

    transactions_by_day = {}
    for t in transactions_raw:
        day = t['date'][-2:]
        if day not in transactions_by_day:
            transactions_by_day[day] = []
        transactions_by_day[day].append(dict(t))

    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    num_days = monthrange(year, month)[1]
    first_day_of_week = monthrange(year, month)[0]
    
    username = session.get('username')

    return render_template(
        'view.html',
        username=username,
        year=year,
        month=month,
        transactions=transactions_by_day,
        prev_month=prev_month,
        prev_year=prev_year,
        next_month=next_month,
        next_year=next_year,
        num_days=num_days,
        first_day=first_day_of_week
    )

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
