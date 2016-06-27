import sqlite3
import os
import re
import logging

class PixnetDB(object):
    sql_files = {
        "pixnet_aritcles": "create_articles_table.sql",
        "pixnet_authors": "create_authors_table.sql"
    }

    def __init__(self):
        self.dbname = 'pixnet.db'
        self.sql_conn = sqlite3.connect(self.dbname)
        self._create_tables(self.sql_conn.cursor())


    def _create_tables(self, cursor):
        for name, filename in self.sql_files.items():
            self._create_table(name, filename, cursor)

    def _create_table(self, tablename, filename, cursor):
        logging.info("Create table %s.", tablename)
        with open(self._getSQLFile(filename), 'r') as f:
            sqlContext = f.read()

        cursor.execute(sqlContext)
        self.sql_conn.commit()

    # Create Sqlite Tables
    def _getSQLFile(self, name):
        dirname = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dirname, 'sql', name)

    def exist_author(self, author_id):
        c = self.sql_conn.cursor()
        c.execute("SELECT * FROM pixnet_aritcles WHERE author_id = ?", (author_id, ))

        data = c.fetchone()
        if data is None:
            return False
        else:
            return True

    def exist_article_link(self, link):
        c = self.sql_conn.cursor()
        c.execute("SELECT link FROM pixnet_aritcles WHERE link = ?", (link, ))

        data = c.fetchone()
        if data is None:
            return False
        else:
            return True

    def store_article_data(self, data):
        c = self.sql_conn.cursor()
        if self.exist_article_link(data[1]):
            pass
        else:
            c.execute("insert into pixnet_aritcles values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
            self.sql_conn.commit()

    def get_all_aritcles_data(self):
        c = self.sql_conn.cursor()
        c.execute("SELECT * FROM pixnet_aritcles")
        return c.fetchall()

    def get_articles_data(self, colname, condition):
        c = self.sql_conn.cursor()
        if re.match('\w+', colname):
            sql = "SELECT * FROM pixnet_aritcles WHERE %s = ?" % (colname)
            c.execute(sql, (condition, ))
            return c.fetchall()
        else:
            logging.error("Column name contains invalid characters.")
            return None

    def close(self):
        self.sql_conn.close()
