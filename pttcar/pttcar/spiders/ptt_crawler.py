import scrapy
from bs4 import BeautifulSoup
from pttcar.items import PttcarItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class Pttcar(CrawlSpider):
    name = 'pttcar'
    start_urls = ['https://www.ptt.cc/bbs/car/index.html']
    rules = [
        Rule(LinkExtractor(allow=('/index[1-3].html')), callback = 'parse_list', follow = True)
    ]
    def parse_list(self, response):
        domain = 'https://www.ptt.cc/'
        res = BeautifulSoup(response.body) #用BeautifulSoup剖析網頁內容
        for news in res.select('.title'): #標題都在class='title'中
            # print(news.select('a')[0].text)
            print(domain + news.select('a')[0]['href'])
            yield scrapy.Request(domain + news.select('a')[0]['href'], self.parse_detail) #用yield去訪問每個連結將內容回給parse_detail

    def parse_detail(self, response): #用parse_detail去剖析裡面的內容，送到pipeline再到mongodb(帶著item裡的欄位進去)
        res = BeautifulSoup(response.body)
        pttcaritem = PttcarItem()  #定義pttcaritem類別，建立pttcaritem物件，把資料放進去
        pttcaritem['title'] = res.select('.article-meta-value')[2].text
        pttcaritem['text'] = res.select('#main-content')[0].text.split('--')[0]
        pttcaritem['time'] = res.select('.article-meta-value')[3].text
        return pttcaritem
