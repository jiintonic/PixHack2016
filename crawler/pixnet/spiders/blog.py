# -*- coding: utf-8 -*-
import scrapy
import sys
import time
import datetime
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Tag
from pixnet.items import PixnetItem
from pixnet.pixnetdb import PixnetDB

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
    db = PixnetDB()

    def parse(self, response):
        for path in response.xpath('//ul[@id="navigation"]/li/ul/li'):
            cat_url = path.xpath('a/@href').extract().pop()
            cat_name = path.xpath('a/text()').extract().pop()

            if cat_name in target_category:
                yield scrapy.Request(self.pixnet_url_prefix + cat_url, callback = self.parse_category)

    def parse_category(self, response):
        for path in response.xpath('//div[@class="box-body"]/div[1]'):
            cat_url = path.xpath('a/@href').extract().pop()
            yield scrapy.Request(cat_url, callback = self.parse_blog_content)

    def parse_blog_content(self, response):
        if self._is_secret_aritcle:
            return

        item = self._get_blog_item(response)
        #yield item

        link = self._get_next_link(response)
        if link is not "":
            print "[NEXT]" + link
            yield scrapy.Request(link, callback = self.parse_blog_content)

        link = self._get_prev_link(response)
        if link is not "":
            print "[PREV]" + link
            yield scrapy.Request(link, callback = self.parse_blog_content)

    def _is_secret_aritcle(self, soup):
        if soup.find('ul', {"class" : "secret-code-notify"}):
            return True
        else:
            return False

    def _get_blog_item(self, response):
        item = PixnetItem()

        item['date'] = self._extract_publish_timestamp(response)
        item['title'] = self._extract_title(response)
        item['article_id'] = self._extract_article_id(response)
        item['link'] = response.url
        item['tags'] = self._extract_tags(response)
        item['pixnet_category'] = self._extract_pixnet_category(response)
        item['personal_category'] = self._extract_personal_category(response)
        item['author_id'] = self._extract_author_id(response)
        item['author_name'] = self._extract_author_name(response)
        item['site_name'] = self._extract_site_name(response)
        item['content'] = self._extract_content(response)

        return item

    def _get_next_link(self, soup):
        find = soup.find('a', {"class": "quick-nav--next"})
        if find:
            link = find.get("href")
        else:
            link = ""

        if not self.db.exist_article_link(link):
            return link
        else:
            return ""

    def _get_prev_link(self, soup):
        find = soup.find('a', {"class": "quick-nav--pre"})
        if find:
            link = find.get("href")
        else:
            link = ""

        if not self.db.exist_article_link(link):
            return link
        else:
            return ""

    def _extract_publish_timestamp(self, response):
        pub_month = response.xpath('//span[@class="month"]/text()').extract_first()
        pub_date = response.xpath('//span[@class="date"]/text()').extract_first()
        pub_day = response.xpath('//span[@class="day"]/text()').extract_first()
        pub_year = response.xpath('//span[@class="year"]/text()').extract_first()
        pub_time = response.xpath('//span[@class="time"]/text()').extract_first()
        date_string = "%s %s %s %s" % (pub_year, pub_month, pub_date, pub_time)

        timestamp = time.mktime(datetime.datetime.strptime(date_string, \
            "%Y %b %d %H:%M").timetuple())

        return timestamp

    def _extract_title(self, response):
        extract = response.xpath('//title/text()').extract_first()
        title = unicode(extract.split("@")[0])
        return title

    def _extract_article_id(self, response):
        extract = response.xpath('//body/@data-article-id').extract_first()
        article_id = long(extract)
        return article_id

    def _extract_tags(self, response):
        extract = response.xpath('//a[@rel="tag"]/text()').extract()
        tags = []

        for tag in extract:
            tags.append(unicode(tag))

        return tags

    def _extract_pixnet_category(self, response):
        extract = response.xpath('//ul[@class="refer"]/li/a/text()').extract_first()
        category = unicode(extract)
        return category

    def _extract_personal_category(self, response):
        extract = response.xpath('//ul[@class="refer"]/li/a/text()').extract()[1]
        category = unicode(extract)
        return category

    def _extract_author_id(self, response):
        extract = response.xpath('//meta[@name="author"]/@content').extract_first()
        author_id = extract.split('(')[0][0:-1]
        return author_id

    def _extract_author_name(self, response):
        extract = response.xpath('//meta[@name="author"]/@content').extract_first()
        author_name = unicode(extract.split('(')[1][0:-1])
        return author_name

    def _extract_site_name(self, response):
        extract = response.xpath('//meta[@property="og:site_name"]/@content').extract_first()
        site_name = unicode(extract)
        return site_name

    def _extract_content(self, response):
        article = ""

        for line in response.xpath('//p').extract():
            soup = BeautifulSoup(line)
            if self._need_skip_line(soup.p):
                continue
            elif 'script' in line:
                continue

            raw_text = unicode(soup.text) + '\n'
            if raw_text.startswith("Skip to article") \
                or raw_text.startswith("Global blog category"):
                continue
            elif raw_text.startswith("Posted by"):
                break
            elif raw_text.strip() == '':
                continue
            else:
                article += raw_text

        return article

    def _need_skip_line(self, soup):
        if type(soup.contents[0]) is Tag:
            if soup.contents[0].name == 'a' :
                return True
            elif soup.contents[0].name == 'img':
                return True
            else:
                return False
        elif soup.find('script') is not None:
            return True
        else:
            return False
