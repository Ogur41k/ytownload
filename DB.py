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

    def create_table_lang(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS lang
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT,
                           language TEXT)''')
        self.conn.commit()

    def create_table_urls(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS channels
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           url TEXT,
                           channel_id TEXT)''')
        self.conn.commit()

    def add(self, text: str, from_user: str, chat_id: str, to_bot: str):
        time = datetime.now()
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO messages (text, from_user, chat_id, to_bot, time) VALUES (?, ?, ?, ?, ?)",
                       (text, from_user, chat_id, to_bot, time))
        self.conn.commit()

    def get_lang(self, user: str):
        cursor = self.conn.cursor()
        return cursor.execute(f"SELECT language FROM lang WHERE username='{user}'").fetchall()[0][0]

    def add_lang(self, user: str, lang: str):
        cursor = self.conn.cursor()
        if len(cursor.execute(f"SELECT language FROM lang WHERE username='{user}'").fetchall()) == 0:
            cursor.execute("INSERT INTO lang (username, language) VALUES (?, ?)",
                           (user, lang))
        else:
            cursor.execute(f"UPDATE lang set language = '{lang}' WHERE username = '{user}'")
        self.conn.commit()

    def get_urls(self):
        cursor = self.conn.cursor()
        return cursor.execute("SELECT url,channel_id FROM channels").fetchall()

    def clear_db(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM messages;")
        cursor.execute("DELETE FROM lang;")
        self.conn.commit()

    def get_users_count(self):
        return self.conn.cursor().execute("SELECT COUNT(DISTINCT from_user) FROM messages;").fetchall()[0][0]


if __name__ == '__main__':
    db = DataBase()
    print(db.get_urls())
