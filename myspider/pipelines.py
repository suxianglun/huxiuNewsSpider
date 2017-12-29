# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import copy
from scrapy.exceptions import DropItem

# 以Json的形式存储


class JsonWithEncodingCnblogsPipeline(object):
    def __init__(self):
        self.file = codecs.open('items.json', 'w', encoding='utf-8')
        self.news_set=set()

    # def process_item(self, item, spider):
    #     line = json.dumps(dict(item), ensure_ascii=False) + "\n"
    #     self.file.write(line)
    #     return item
    def process_item(self, item, spider):
        title = item['title']
        if title in self.news_set:
            # raise 强制抛出异常
            raise DropItem('Duplicate news found %s' % item)
        self.news_set.add(title)
        return item

    #pipeline默认调用 解决保存重复数据的问题
    # def process_item(self, item, spider):
    #     # 深拷贝
    #     asynItem = copy.deepcopy(item)
    #     d = self.dbpool.runInteraction(self._do_upinsert, asynItem, spider)
    #     return asynItem


    def spider_closed(self, spider):
        self.file.close()

