import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor
from policyCrawler.items import PolicyCrawlerNewsItem
from scrapy.loader import ItemLoader
import time
from hashlib import md5


class NeaGovCn(CrawlSpider):
    name = "Nea_Gov_cn"

    start_urls = ["http://www.nea.gov.cn/"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    }

    rules = (
        Rule(
            LinkExtractor(allow=("http\:\/\/www\.nea\.gov\.cn\/\d{1,4}\-\d{1,2}\/\d{1,2}\/.*?\.htm",)),
            callback="parse_content",
            follow=True),
        Rule(
            LinkExtractor(allow=("http\:\/\/www\.nea\.gov\.cn\/.*?",)),
            follow=True),
    )

    def start_requests(self):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, headers=self.headers)

    def parse_content(self, response):

        def deal_publish_time(publishTimeRaw):
            try:
                year = str(publishTimeRaw[0])
                mouth = str(publishTimeRaw[1])
                days = str(publishTimeRaw[2])

                return year + "-" + mouth + "-" + days + " 00:00:00"
            except Exception as e:
                print(e)
                return "2018-02-01 00:00:00"

        def deal_artilce_from(article_from_L):
            try:
                article_from_str1 = ".".join(article_from_L)
                article_from = article_from_str1.strip(':')[1].strip()
                return article_from
            except Exception as e:
                print(e)
                return ''

        content_loader = ItemLoader(
            response=response,
            item=PolicyCrawlerNewsItem())
        content_loader.add_value("website_name", "国家能源局官网")
        content_loader.add_value("spider_time", int(time.time()))
        content_loader.add_value("spider_name", self.name)
        content_loader.add_value("url", response.url)
        content_loader.add_value("url_md5",
                                 md5(response.url.encode("utf-8")).digest())
        content_loader.add_xpath("title",
                                 "//div[@class='main-colum']//div[@class='titles']/text()",
                                 lambda x: ".".join([x1.strip() for x1 in x]))
        content_loader.add_xpath(
            "content",
            "//div[@class='main-colum']//div[@class='article-box']//td//text()",
            lambda x: '.'.join(
                x1.strip() for x1 in x))
        content_loader.add_value("article_from", response.xpath(
            "//div[@class='main-colum']//span[@class='author']/text()"), deal_artilce_from)
        content_loader.add_value(
            "publish_time",
            response.xpath("//div[@class='main-colum']//span[@class='times']//text()").re("(\d{4})\-(\d{2})\-(\d{2})"),
            deal_publish_time)
