# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from doubanscrapy.model import Model


class DoubanscrapyPipeline(object):
    def open_spider(self, spider):
        self.file = open('test.json', 'w')

    def close_spider(self):
        self.file.close()

    def process_item(self, item, spider):
        try:
            Model.saveMovie(item)
        except Exception:
            pass
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item
