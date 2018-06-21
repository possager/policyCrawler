# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PolicycrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PolicyCrawlerNewsItem(scrapy.Item):
    website_name = scrapy.Field()
    spider_time = scrapy.Field()
    publish_time = scrapy.Field()
    url_md5 = scrapy.Field()
    url = scrapy.Field()
    document_urls=scrapy.Field()

    publish_timestamp = scrapy.Field()
    article_from = scrapy.Field()
    content = scrapy.Field()
    title = scrapy.Field()
    reply_count = scrapy.Field()
    read_count = scrapy.Field()
    img_urls = scrapy.Field()

    channel_id = scrapy.Field()
    params = scrapy.Field()
    id = scrapy.Field()
    channel_name = scrapy.Field()
    abstract = scrapy.Field()
    publish_user = scrapy.Field()
    reproduce_count = scrapy.Field()
    video_urls = scrapy.Field()
    dislike_count = scrapy.Field()
