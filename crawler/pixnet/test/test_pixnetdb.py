#!/usr/bin/python

import os
import sys
import unittest
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from pixnetdb import PixnetDB


class PixnetDBTest(unittest.TestCase):

    def setUp(self):
        self.db = PixnetDB()

    def test_exist_author(self):
        author_id = 'weio851015'
        self.assertTrue(self.db.exist_author(author_id))

    def test_exist_article_link(self):
        link = 'http://weio851015.pixnet.net/blog/post/379678318'
        self.assertTrue(self.db.exist_article_link(link))

    '''
    def test_get_all_articles_data(self):
        data = self.db.get_all_aritcles_data()
        print data
    '''


    def tearDown(self):
        self.db.close()



if __name__ == '__main__':
	unittest.main()
