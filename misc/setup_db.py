import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('MESSAGES_DB')
print(f"Setting up database: {db_path}")

# Создаем директорию если её нет
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Удаляем таблицу если она существует
cursor.execute("DROP TABLE IF EXISTS messages")

# Создаем таблицу заново
cursor.execute("""
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message TEXT NOT NULL,
    timestamp REAL NOT NULL,
    token TEXT NOT NULL DEFAULT ''
)
""")

conn.commit()
conn.close()

print("Database setup complete!")