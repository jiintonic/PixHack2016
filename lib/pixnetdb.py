import sqlite3
import os
import re
import logging
import time
from lib import reverse_url

class PixnetDB(object):
    sql_files = {
        "pixnet_aritcles": "create_articles_table.sql",
        "pixnet_authors": "create_authors_table.sql"
    }

    db_name = 'pixnet.db'

    def __init__(self):
        pixhak_path = os.environ.get('PIXHACK_PATH')
        if pixhak_path:
            db_path = os.path.join(pixhak_path, self.db_name)
        else:
            db_path = db_name

        self.sql_conn = sqlite3.connect(db_path)
        self._create_tables(self.sql_conn.cursor())

    def _create_tables(self, cursor):
        for name, filename in self.sql_files.items():
            self._create_table(name, filename, cursor)

    def _create_table(self, tablename, filename, cursor):
        logging.info("Create table %s.", tablename)
        with open(self._get_sql_file(filename), 'r') as f:
            sqlContext = f.read()

        cursor.execute(sqlContext)
        self.sql_conn.commit()

    def _get_sql_file(self, name):
        sql_dir = os.environ.get('SQL_PATH')
        if sql_dir:
            return os.path.join(sql_dir, name)
        else:
            dirname = os.path.dirname(os.path.realpath(__file__))
            return os.path.join(dirname, 'sql', name)

    def exist_article_link(self, link):
        rlink = reverse_url(link)
        c = self.sql_conn.cursor()
        c.execute("SELECT link FROM pixnet_aritcles WHERE link = ?", (rlink, ))

        data = c.fetchone()
        if data is None:
            return False
        else:
            return True

    def exist_article_id(self, article_id):
        c = self.sql_conn.cursor()
        c.execute("SELECT link FROM pixnet_aritcles WHERE article_id = ?", (article_id, ))

        data = c.fetchone()
        if data is None:
            return False
        else:
            return True

    def store_article_data(self, data):
        c = self.sql_conn.cursor()
        link = data[1]

        if self.exist_article_link(link):
            pass
        else:
            c.execute("INSERT INTO pixnet_aritcles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
            self.sql_conn.commit()

    def get_article_count(self):
        c = self.sql_conn.cursor()
        c.execute("SELECT count(*) FROM pixnet_aritcles")
        return c.fetchone()

    def get_all_aritcle_data(self):
        c = self.sql_conn.cursor()
        c.execute("SELECT * FROM pixnet_aritcles")
        return c.fetchall()

    def get_article_data(self, article_id):
        c = self.sql_conn.cursor()

        sql = "SELECT * FROM pixnet_aritcles WHERE article_id = ?"
        c.execute(sql, (article_id, ))
        return c.fetchone()

    def get_articles(self):
        c = self.sql_conn.cursor()

        sql = "SELECT content FROM pixnet_aritcles"
        c.execute(sql)
        return c.fetchall()

    def get_articles_by(self, column, condition):
        c = self.sql_conn.cursor()
        if re.match('[\w_]+', column):
            sql = "SELECT content FROM pixnet_aritcles WHERE %s = ?" % (column)
            c.execute(sql, (condition, ))
            return c.fetchall()
        else:
            logging.error("Column name contains invalid characters.")
            return None

    def delete_article_data(self, article_id):
        c = self.sql_conn.cursor()
        sql = "DELETE FROM pixnet_aritcles WHERE article_id = ?"
        c.execute(sql, (article_id, ))
        self.sql_conn.commit()

    def exist_author(self, author_id):
        c = self.sql_conn.cursor()
        c.execute("SELECT * FROM pixnet_authors WHERE author_id = ?", (author_id, ))

        data = c.fetchone()
        if data is None:
            return False
        else:
            return True

    def store_author_data(self, data):
        c = self.sql_conn.cursor()
        author_id = data[0]

        if self.exist_author(author_id):
            self.update_author_data(data)
        else:
            c.execute("INSERT INTO pixnet_authors VALUES (?, ?, ?, ?, ?, ?, ?)", data)
            self.sql_conn.commit()

    def get_all_author_data(self):
        c = self.sql_conn.cursor()
        c.execute("SELECT * FROM pixnet_authors")
        return c.fetchall()

    def get_author_data(self, author_id):
        c = self.sql_conn.cursor()
        sql = "SELECT * FROM pixnet_authors WHERE author_id = ?"
        c.execute(sql, (author_id, ))
        return c.fetchone()

    def get_author_count(self):
        c = self.sql_conn.cursor()
        c.execute("SELECT count(*) FROM pixnet_authors")
        return c.fetchone()

    def update_author_data(self, data):
        sql = "UPDATE pixnet_authors SET last_update_date = ?, last_article_link = ? WHERE author_id = ?"
        c = self.sql_conn.cursor()
        author_id = data[0]
        last_update = data[5]
        last_article_link = data[6]

        c.execute(sql, (last_update, last_article_link, author_id))
        self.sql_conn.commit()

    def delete_author_data(self, author_id):
        c = self.sql_conn.cursor()
        sql = "DELETE FROM pixnet_authors WHERE author_id = ?"
        c.execute(sql, (author_id, ))
        self.sql_conn.commit()

    def close(self):
        self.sql_conn.close()
