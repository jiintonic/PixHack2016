# -*- coding: utf-8 -*-
import scrapy
import sys
import time
import datetime
from BeautifulSoup import BeautifulSoup

from pixnet.items import PixnetItem

target_category = [
    u"國內旅遊",
    u"國外旅遊",
    u"時尚流行",
    u"美容彩妝"
]

class BlogSpider(scrapy.Spider):
    name = "blog"
    allowed_domains = ["pixnet.net"]
    pixnet_url_prefix = "https://www.pixnet.net"
    start_urls = (
        pixnet_url_prefix + '/blog',
    )

    def parse(self, response):
        for path in response.xpath('//ul[@id="navigation"]/li/ul/li'):
            cat_url = path.xpath('a/@href').extract().pop()
            cat_name = path.xpath('a/text()').extract().pop()

            if cat_name in target_category:
                print cat_name, cat_url
                yield scrapy.Request(self.pixnet_url_prefix + cat_url, callback = self.parse_category)

    def parse_category(self, response):
        for path in response.xpath('//div[@class="box-body"]/div[1]'):
            cat_url = path.xpath('a/@href').extract().pop()
            print cat_url
            yield scrapy.Request(cat_url, callback = self.parse_blog_content)

    def parse_blog_content(self, response):
        item = PixnetItem()
        item['date'] = self.__parse_blog_publish_timestamp(response)
        item['title'] = response.xpath('//title/text()').extract_first() \
            .split("@")[0]
        item['article_id'] = response.xpath('//body/@data-article-id').extract_first()
        item['link'] = response.url
        item['tags'] = response.xpath('//a[@rel="tag"]/text()').extract()
        item['pixnet_category'] = response.xpath('//ul[@class="refer"]/li/a/text()').extract_first()
        item['personal_category'] = response.xpath('//ul[@class="refer"]/li/a/text()').extract()[1]
        author = response.xpath('//meta[@name="author"]/@content').extract_first()
        item['author_id'] = author.split('(')[0][0:-1]
        item['author_name'] = author.split('(')[1][0:-1]
        item['site_name'] = response.xpath('//meta[@property="og:site_name"]/@content').extract_first()

        with open('%s.txt' % item['article_id'],"w+") as f:
            for line in response.xpath('//p').extract():
                raw_text = BeautifulSoup(line).text.encode("utf-8")+'\n'
                if raw_text.startswith("Skip to article") \
                    or raw_text.startswith("Global blog category"):
                    continue
                elif raw_text.startswith("Posted by"):
                    break
                else:
                    f.write(raw_text)

        yield item

    def __parse_blog_publish_timestamp(self, response):
        pub_month = response.xpath('//span[@class="month"]/text()').extract_first()
        pub_date = response.xpath('//span[@class="date"]/text()').extract_first()
        pub_day = response.xpath('//span[@class="day"]/text()').extract_first()
        pub_year = response.xpath('//span[@class="year"]/text()').extract_first()
        pub_time = response.xpath('//span[@class="time"]/text()').extract_first()
        date_string = "%s %s %s %s" % (pub_year, pub_month, pub_date, pub_time)

        local_timestamp = time.mktime(datetime.datetime.strptime(date_string, \
            "%Y %b %d %H:%M").timetuple())

        return local_timestamp
