# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HuxiuItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()  # 标题
    link = scrapy.Field()   # 链接
    author = scrapy.Field()   # 作者
    desc = scrapy.Field()   # 简述
    post_time = scrapy.Field()  # 发布时间
    pic_url = scrapy.Field()  # 文章头图
    content = scrapy.Field()  # 内容

    pass
