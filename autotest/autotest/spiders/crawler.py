import scrapy
from bs4 import BeautifulSoup
from autotest.items import AutotestItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class AutotestCrawler(CrawlSpider):
    name = 'autotest'
    # allowed_domains = ['auto.ltn.com.tw']
    start_urls = ['https://auto.ltn.com.tw/list/43/']
    rules = [
        Rule(LinkExtractor(allow=('/list/43/[1-3]$')), callback='parse_list', follow=True)
    ]
    def parse_list(self, response):
        res = BeautifulSoup(response.body)
        for news in res.select('.newsunit2'):
            # print(news.select('a.title')[0].text)
            # print(news.select('a')[0]['href'])
            yield scrapy.Request(news.select('a')[0]['href'], self.parse_detail)

    def parse_detail(self, response):
        res = BeautifulSoup(response.body)
        autotestitem = AutotestItem()
        autotestitem['title'] = res.select('h1')[0].text
        autotestitem['text'] = res.select('.article')[0].text.split('\n\n\n\n\n\n\n\n\n\n\n\n\n')[1]\
                                .replace('請繼續往下閱讀... \n\n\n\n\n\n\n\n', '')
        autotestitem['time'] = res.select('.time')[0].text
        return autotestitem



