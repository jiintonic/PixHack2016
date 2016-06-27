# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import sys
import os
import logging
from pixnetdb import PixnetDB

class SqlitePipeline(object):
    db = None

    def _tags_to_string(self, tags):
        tag_str = ""
        for tag in tags:
            tag_str += tag + ','

        tag_str = tag_str[0:-1]
        return tag_str

    def _store_aritcle(self, item):
        article_data = (
            item['title'], \
            item['link'], \
            item['content'], \
            self._tags_to_string(item['tags']), \
            item['pixnet_category'], \
            item['personal_category'], \
            0, \
            item['article_id'], \
            item['author_id'], \
            item['date'] \
        )
        self.db.store_article_data(article_data)

        return

    # Scrapy Pipline
    def process_item(self, item, spider):

        self._store_aritcle(item)

        return item

    def open_spider(self, spider):
        try:
            self.db = PixnetDB()
        except:
            logging.error(str(sys.exc_info()))

        return

    def close_spider(self, spider):
        self.db.close()
        return
