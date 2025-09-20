from flask import Flask, request, redirect, url_for, render_template, session
from datetime import datetime, date
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from calendar import monthrange

app = Flask(__name__)
app.secret_key = 'my_super_secret_key'

# 이 부분은 Vercel에서는 작동하지 않으므로 비활성화합니다.
def get_db_connection():
    pass

def init_db():
    pass

# init_db()

def register_user(username, password):
    # 이 함수는 데이터베이스가 없어 작동하지 않습니다.
    return False

def check_user(username, password):
    # 이 함수는 데이터베이스가 없어 작동하지 않습니다.
    return None

def add_transaction(user_id, date, item, amount):
    # 이 함수는 데이터베이스가 없어 작동하지 않습니다.
    pass

def get_transactions_by_user(user_id):
    # 이 함수는 데이터베이스가 없어 작동하지 않습니다.
    return []

def get_balance(user_id):
    # 이 함수는 데이터베이스가 없어 작동하지 않습니다.
    return 0

@app.route('/')
def home():
    return "<h1>Welcome to my-budget!</h1>"

@app.route('/register', methods=['GET', 'POST'])
def register():
    return "<h1>등록 기능은 현재 비활성화되었습니다.</h1>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    return "<h1>로그인 기능은 현재 비활성화되었습니다.</h1>"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    return "<h1>지출 추가 기능은 현재 비활성화되었습니다.</h1>"

@app.route('/view')
def view():
    return "<h1>보기 기능은 현재 비활성화되었습니다.</h1>"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')