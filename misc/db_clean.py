import os
import sqlite3
from dotenv import load_dotenv


load_dotenv()


def quote_identifier(identifier):
    return '"' + identifier.replace('"', '""') + '"'


def clear_tables(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = OFF;")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = cursor.fetchall()

    for table in tables:
        accept = input(f"Clean table {table}? (y/n): ").strip().lower()
        if accept != 'y':
            return
        table_name = table[0]
        query = f"DELETE FROM {quote_identifier(table_name)};"
        print(f"Очищаю таблицу: {table_name}")
        cursor.execute(query)

        try:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name = ?;", (table_name,))
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()


def main():
    clear_tables('../' + os.getenv('MESSAGES_DB'))


if __name__ == '__main__':
    main()
