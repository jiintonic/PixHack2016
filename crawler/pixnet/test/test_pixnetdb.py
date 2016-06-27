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
        author_id = 'cheers090'
        self.assertTrue(self.db.exist_author(author_id))

    def test_exist_article_link(self):
        link = 'http://cheers090.pixnet.net/blog/post/328297671-%e5%a2%be%e4%b8%81%e6%97%85%e9%81%8a%e2%98%bc%e5%a4%8f%e6%97%a5%e4%be%86%e5%a0%b4%e5%a5%a2%e8%8f%af%e9%81%8a%e8%89%87party%21%21%21-%e4%bc%8a%e4%ba%9e%e9%81%8a%e8%89%87'
        self.assertTrue(self.db.exist_article_link(link))

    def test_modify_article_data(self):
        article_data = (
            'test_title',
            'http://test.link.com/',
            'This is content of test article.',
            'tag1,tag2',
            'test_category',
            'personal_category',
            0,
            1234,
            'raix',
            12345678
        )
        article_content = article_data[2]
        article_id = article_data[7]

        # Test insert article data
        self.db.store_article_data(article_data)
        self.assertTrue(self.db.exist_article_id(article_id))

        # Test get article data
        select = self.db.get_article_data(article_id)
        for i in range(len(article_data)):
            self.assertEqual(article_data[i], select[i])

        # Test get article content by article id
        select = self.db.get_articles_by("article_id", article_id)
        self.assertEqual(article_content, select[0][0])

        # Test delete article data
        self.db.delete_article_data(article_id)
        self.assertFalse(self.db.exist_article_id(article_id))

    def test_modify_author_data(self):
        author_data = (
            'raix',
            'raix lai',
            'Raix blog',
            0,
            12345678,
            12345678,
            'http://test.link.com/'
        )
        author_id = author_data[0]

        # Test insert author data
        self.db.store_author_data(author_data)
        self.assertTrue(self.db.exist_author(author_id))

        # Test get author data
        select = self.db.get_author_data(author_id)
        for i in range(len(author_data)):
            self.assertEqual(author_data[i], select[i])

        # Test modify author data
        modify_data = (
            'raix',
            'raix lai',
            'Raix blog',
            0,
            12345678,
            12345700,
            'http://test.link.com/modify'
        )
        self.db.update_author_data(modify_data)
        select = self.db.get_author_data(author_id)
        for i in range(len(modify_data)):
            self.assertEqual(modify_data[i], select[i])

        # Test delete author data
        self.db.delete_author_data(author_id)
        self.assertFalse(self.db.exist_author(author_id))

    def tearDown(self):
        self.db.close()

if __name__ == '__main__':
	unittest.main()
