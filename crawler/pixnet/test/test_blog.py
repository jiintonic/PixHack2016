#!/usr/bin/python

import os
import sys
import unittest
from BeautifulSoup import BeautifulSoup
sys.path.insert(1, os.path.join(sys.path[0], '../../'))
from pixnet.spiders.blog import BlogSpider

class BlogTest(unittest.TestCase):

    def setUp(self):
        self.spider = BlogSpider()

        dirname = os.path.dirname(os.path.realpath(__file__))
        test_file_1 = os.path.join(dirname, 'testcase/329049123.html')
        with open(test_file_1, 'r') as f:
            html = f.read()
            self.soup1 = BeautifulSoup(html)

        test_file_2 = os.path.join(dirname, 'testcase/43919692.html')
        with open(test_file_2, 'r') as f:
            html = f.read()
            self.soup2 = BeautifulSoup(html)

    def test_is_secret_aritcle(self):
        self.assertTrue(self.spider._is_secret_aritcle(self.soup1))
        self.assertFalse(self.spider._is_secret_aritcle(self.soup2))

    def test_get_next_link(self):
        self.assertEqual("", self.spider._get_next_link(self.soup1))
        self.assertEqual("", self.spider._get_next_link(self.soup2))

    def test_get_prev_link(self):
        self.assertEqual("", self.spider._get_prev_link(self.soup1))
        self.assertEqual("http://bajenny.pixnet.net/blog/post/43823356-2016%e5%ae%9c%e8%98%ad%e5%9c%8b%e9%9a%9b%e7%ab%a5%e7%8e%a9%e7%af%80%7e%e7%ab%a5%e7%8e%a9%e7%af%80%e5%ae%9c%e8%98%ad%e6%b0%91%e5%ae%bf-%e5%ae%9c%e8%98%ad%e9%a3%af%e5%ba%97", \
            self.spider._get_prev_link(self.soup2))

    def tearDown(self):
        pass

if __name__ == '__main__':
	unittest.main()
