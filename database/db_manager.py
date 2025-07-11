import sqlite3

DB_PATH = "./dscpl.db"

def create_reminders_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            message TEXT NOT NULL,
            reminder_time TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_reminder(user_id: str, message: str, reminder_time: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO reminders (user_id, message, reminder_time) VALUES (?, ?, ?)',
                (user_id, message, reminder_time))
    conn.commit()
    conn.close()

def get_reminders_at_time(current_time: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT user_id, message FROM reminders WHERE reminder_time = ?', (current_time,))
    rows = cur.fetchall()
    conn.close()
    return rows

def get_user_reminders(user_id: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT message, reminder_time FROM reminders WHERE user_id = ?', (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows
