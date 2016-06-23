# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PixnetItem(scrapy.Item):
    date = scrapy.Field()
    title =  scrapy.Field()
    link = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    pixnet_category = scrapy.Field()
    personal_category = scrapy.Field()
    article_count = scrapy.Field()
    article_id = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    site_name = scrapy.Field()
