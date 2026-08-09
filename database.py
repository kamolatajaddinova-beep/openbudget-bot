import sqlite3

def init_db():
    conn = sqlite3.connect("open_budget.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            phone TEXT,
            balance REAL DEFAULT 0.0,
            referrer_id INTEGER,
            votes_count INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, referrer_id=None):
    conn = sqlite3.connect("open_budget.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id, referrer_id) VALUES (?, ?)", (user_id, referrer_id))
    conn.commit()
    conn.close()

def update_user_vote(user_id, phone, reward=15000):
    conn = sqlite3.connect("open_budget.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users 
        SET phone = ?, balance = balance + ?, votes_count = votes_count + 1 
        WHERE user_id = ?
    """, (phone, reward, user_id))
    conn.commit()
    conn.close()

def get_user_data(user_id):
    conn = sqlite3.connect("open_budget.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance, votes_count FROM users WHERE user_id = ?", (user_id,))
    data = cursor.fetchone()
    conn.close()
    return data if data else (0.0, 0)
