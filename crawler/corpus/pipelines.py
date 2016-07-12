# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from codecs import open
import re

class CorpusPipeline(object):
    # def __init__(self):
        # self.file = open('.txt', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        self.file = open(str(spider.name)+'.txt', 'a', encoding='utf-8')
        for line in item['text']:
            line = re.sub(r'[ \n]+', ' ', line)
            if not line:
                continue
            self.file.write(line)
        self.file.write('\n')
        return item
