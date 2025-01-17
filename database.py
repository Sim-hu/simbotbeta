# database.py

import sqlite3
from datetime import datetime
import os
from dotenv import load_dotenv

# 環境変数のロード
load_dotenv()

# 環境変数からデータベース名を取得
DB_NAME = os.getenv('DB_NAME')

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS user_balances
                 (user_id TEXT PRIMARY KEY, balance INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_daily
                 (user_id TEXT PRIMARY KEY, last_daily TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_balance(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT balance FROM user_balances WHERE user_id=?", (str(user_id),))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        set_balance(user_id, 1000)
        return 1000

def set_balance(user_id, balance):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO user_balances (user_id, balance) VALUES (?, ?)",
              (str(user_id), balance))
    conn.commit()
    conn.close()

def get_last_daily(user_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT last_daily FROM user_daily WHERE user_id=?", (str(user_id),))
    result = c.fetchone()
    conn.close()
    if result:
        return datetime.fromisoformat(result[0])
    return None

def set_last_daily(user_id, timestamp):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO user_daily (user_id, last_daily) VALUES (?, ?)",
              (str(user_id), timestamp.isoformat()))
    conn.commit()
    conn.close()

def get_all_balances():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT user_id, balance FROM user_balances")
    balances = c.fetchall()
    conn.close()
    return balances