import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv('MESSAGES_DB')
print(f"Checking database: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получаем информацию о структуре таблицы
cursor.execute("PRAGMA table_info(messages)")
columns = cursor.fetchall()
print("\nTable structure:")
for col in columns:
    print(f"Column: {col[1]}, Type: {col[2]}, NotNull: {col[3]}, DefaultValue: {col[4]}")

conn.close()