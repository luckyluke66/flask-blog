import sqlite3

class Database():
    def __init__(self):
        self.connection = sqlite3.connect("db.sqlite", isolation_level=None)
        self.connection.row_factory = sqlite3.Row

    def validate_user(self, username, password):
        row = self.connection.execute('SELECT username, password FROM users WHERE username = ? AND password = ?', [username, password])
        return row.fetchone()

    def get_articles(self):
        rows = self.connection.execute('SELECT * FROM articles ORDER BY id DESC')
        return rows.fetchall()

    def inser_article(self, title, content):
        self.connection.execute('INSERT INTO articles (title, content) VALUES (?, ?)', [title, content])

    def get_article_by_id(self, id):
        row = self.connection.execute('SELECT title, content FROM articles WHERE id = ?', [id])
        return row.fetchone()
