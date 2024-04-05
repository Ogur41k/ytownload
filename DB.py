import sqlite3
from datetime import datetime


class DataBase:
    def __init__(self, filename: str = 'database.db'):
        self.conn = sqlite3.connect(filename)
        if not self.table_exist():
            self.create_table()

    def table_exist(self, table_name: str = "messages"):
        cursor = self.conn.cursor()
        return cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)).fetchone()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           text TEXT,
                           from_user TEXT,
                           chat_id TEXT,
                           to_bot TEXT,
                           time TIMESTAMP)''')
        self.conn.commit()

    def add(self, text: str, from_user: str,chat_id:str, to_bot: str):
        time = datetime.now()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO messages (text, from_user, chat_id, to_bot, time) VALUES (?, ?, ?, ?, ?)",
                       (text, from_user, chat_id, to_bot, time))
        self.conn.commit()

    def clear_db(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM messages;")
        self.conn.commit()

    def get_users_count(self):
        return self.conn.cursor().execute("SELECT COUNT(DISTINCT from_user) FROM messages;").fetchall()[0][0]


if __name__ == '__main__':
    db = DataBase()
    print(db.get_users_count())
