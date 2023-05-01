# Database support
import sqlite3

TABLE_NAME = 'vkrss'


class Database:
    def __init__(self):
        self.db_connection = sqlite3.connect(f'./{TABLE_NAME}.sqlite')
        self.db = self.db_connection.cursor()
        self.db.execute(
            f'CREATE TABLE IF NOT EXISTS {TABLE_NAME} (vk_id INT, tg_id INT, date INT)')

    def article_is_not_db(self, id):
        """
        Check post in DB
        """
        self.db.execute(f"SELECT * FROM {TABLE_NAME} WHERE vk_id='{id}'")
        if not self.db.fetchall():
            return True
        return False

    def get_tg_id(self, vk_id):
        """
        Get telegram post id in DB
        """
        self.db.execute(f"SELECT * FROM {TABLE_NAME} WHERE vk_id='{vk_id}'")
        t = self.db.fetchall()
        if t:
            return t[0][1]  # column of tg_id
        return False

    def add_article_to_db(self, vk_id: int, tg_id: int, date: int):
        """
        Add post to DB
        """
        self.db.execute(
            f"INSERT INTO {TABLE_NAME} VALUES ('{vk_id}', '{tg_id}', '{date}')")
        self.db_connection.commit()

    def __del__(self):
        self.db_connection.close()


db = Database()
