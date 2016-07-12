import scrapy
import re
from codecs import open
from corpus.items import Rbc



class Rbc_crawler(scrapy.Spider):
    name = 'rbc'
    offset = 0
    allowed_domains = ['www.rbc.ru']
    start_urls = ['http://www.rbc.ru/search/ajax/?project=rbcnews&offset=5000&limit=10&query=%D0%A0%D0%91%D0%9A']


    def parse(self, response):
        if self.offset < 10000:
            a = re.findall('\"fronturl\":\"(.*?)\",\"publish_date\"', response.body)
            if not a:
                raise TimeoutError
            for link in a:
                yield scrapy.Request(link.replace('\\', ''), callback=self.parse_text)
            
            self.offset += 10
            nexturl = 'http://www.rbc.ru/search/ajax/?project=rbcnews&offset={}&limit=10&query=%D0%A0%D0%91%D0%9A'.format(self.offset+5000)
            yield scrapy.Request(nexturl, callback=self.parse)

        else:
            raise scrapy.exceptions.CloseSpider


    def parse_text(self, response):
        item = Rbc()
        a = response.xpath('..//div[@class="article__text"]/p/descendant-or-self::node()[not(name()="script")]/text()').extract()
        item['text'] = a
        return item
        