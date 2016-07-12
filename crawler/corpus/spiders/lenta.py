# coding=utf-8
import scrapy
from corpus.items import Rbc
import re


class Lenta_crawler(scrapy.Spider):
    name = 'lenta'
    offset = 1
    allowed_domains = ['lenta.ru']
    start_urls = ['https://lenta.ru/search/process?&query=%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9+%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%BE%D1%80']


    def parse(self, response):
        if self.offset < 7000:
            a = re.findall(r'"url": "(.*?)",', response.body)
            for link in a:
                yield scrapy.Request(link.replace('\\', ''), callback=self.parse_text)
            self.offset += 10
            nexturl = 'https://lenta.ru/search/process?start={}&limit=10&sort=2&title_only=0&snp.around=15&domain=1&query=%D0%B3%D0%B5%D0%BD%D0%B5%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9+%D0%B4%D0%B8%D1%80%D0%B5%D0%BA%D1%82%D0%BE%D1%80'.format(self.offset)
            yield scrapy.Request(nexturl, callback=self.parse)

        else:
            raise scrapy.exceptions.CloseSpider


    def parse_text(self, response):
        item = Rbc()
        a = response.xpath('..//div[@class="b-text clearfix"]/p/descendant-or-self::node()[not(name()="script")]/text()').extract()
        item['text'] = a
        return item