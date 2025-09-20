# db_setup.py

import sqlite3

# 1. 데이터베이스 파일 연결 또는 생성하기
conn = sqlite3.connect('my_budget.db')
cursor = conn.cursor()

# 2. 사용자(user) 테이블 생성하기 (transactions 테이블보다 먼저)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# 3. 가계부 내역(transactions) 테이블 생성하기
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        item TEXT NOT NULL,
        amount INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

# 4. 변경사항 저장하고 연결 닫기
conn.commit()
conn.close()

print("데이터베이스와 'users', 'transactions' 테이블이 모두 성공적으로 생성되었습니다.")