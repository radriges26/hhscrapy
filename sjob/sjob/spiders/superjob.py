import scrapy
from pymongo import MongoClient
from bs4 import BeautifulSoup

db = MongoClient(host='localhost', port=27017)
db = db.data_gb_5

class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/']
    pages_count = 5

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f'https://spb.superjob.ru/vakansii/prodavec-kassir.html?page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.css('.f-test-search-result-item .icMQ_::attr("href")').extract():
            url = response.urljoin(href)
            if 'vakansii' in url:
                yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, **kwargs):

        item = {
            'url': response.request.url,
            'title': response.css('.rFbjy::text').extract_first('').strip(),
            'price': BeautifulSoup(response.css('._2Wp8I').extract_first('').strip(), "lxml").text
        }
        db.data.insert(item)
        yield item