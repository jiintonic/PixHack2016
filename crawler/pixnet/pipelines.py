# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import sys
import os

class PixnetPipeline(object):
    def process_item(self, item, spider):
        return item

class SqlitePipeline(object):
    sql_conn = None

    # Create Sqlite Tables
    def _getSQLFile(self, name):
        dirname = os.path.dirname(os.path.realpath(__file__))
        print os.path.join(dirname, 'sql', name)
        return os.path.join(dirname, 'sql', name)

    def _create_tables(self, cursor):
        print "[INFO] Create tables."
        self._create_table('create_authors_table.sql', cursor)
        self._create_table('create_articles_table.sql', cursor)

    def _create_table(self, filename, cursor):
        with open(self._getSQLFile(filename), 'r') as f:
            sqlContext = f.read()

        cursor.execute(sqlContext)
        self.sql_conn.commit()

    def _tags_to_string(self, tags):
        tag_str = ""
        for tag in tags:
            tag_str += tag + ','

        tag_str = tag_str[0:-1]
        return tag_str

    def _store_aritcle(self, item):
        c = self.sql_conn.cursor()

        row_data = [(
            item['title'], \
            item['link'], \
            item['content'], \
            self._tags_to_string(item['tags']), \
            item['pixnet_category'], \
            item['personal_category'], \
            0, \
            item['article_id'], \
            item['date'] \
        )]

        c.executemany('INSERT INTO pixnet_aritcles VALUES (?,?,?,?,?,?,?,?,?)', \
            row_data)

        self.sql_conn.commit()
        return

    # Scrapy Pipline
    def process_item(self, item, spider):


        for k, v in item.items():
            print k, v

        self._store_aritcle(item)

        return item

    def open_spider(self, spider):
        try:
            self.sql_conn = sqlite3.connect('pixnet.db')
            c = self.sql_conn.cursor()
            self._create_tables(c)
        except:
            print 'Error at createDatabase():',str(sys.exc_info())
            print 'failed.'
        finally:
            c.close()
        return

    def close_spider(self, spider):
        self.sql_conn.close()
        return
