import scrapy
from bs4 import BeautifulSoup
from pchome.items import PchomeItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class PchomeCrawler(CrawlSpider):
    name = 'pchome'
    # allowed_domains = ['auto.ltn.com.tw']
    start_urls = ['https://news.pchome.com.tw/cat/car/hot/']
    rules = [
        Rule(LinkExtractor(allow=('/cat/car/hot/[1-3]$')), callback='parse_list', follow=True)
    ]
    def parse_list(self, response):
        res = BeautifulSoup(response.body)
        for news in res.select('div.channel_newssection'):
            # print(news.select('a.title')[0].text)
            # print(news.select('a')[0]['href'])
            yield scrapy.Request('https://news.pchome.com.tw/' + news.select('a')[0]['href'], self.parse_detail)

    def parse_detail(self, response):
        res = BeautifulSoup(response.body)
        pchomeitem = PchomeItem()
        pchomeitem['title'] = res.select('span[id="iCliCK_SafeGuard"]')[0].text
        pchomeitem['text'] = res.select('div[calss="article_text"]')[0].text
        pchomeitem['time'] = res.select('li[class="func_time"]')[0].text
        return pchomeitem

