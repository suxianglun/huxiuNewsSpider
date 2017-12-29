# -*- coding:utf-8 -*-
import copy

import scrapy
import uniout
import time
from myspider.items import HuxiuItem
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


class DmozSpider(scrapy.Spider):
    # 定义spider名字
    name = "huxiu"
    # 减慢爬取速度 为1s
    download_delay = 1
    # 允许爬取的域名(domain)列表(list)。 当 OffsiteMiddleware 启用时， 域名不在列表中的URL不会被跟进。
    allowed_domains = ["huxiu.com"]

    # URL列表。当没有制定特定的URL时，spider将从该列表中开始进行爬取。
    #  因此，第一个被获取到的页面的URL将是该列表之一。 后续的URL将会从获取到的数据中提取

    start_urls = [
        "http://www.huxiu.com/index.php/",
    ]
    # 该方法必须返回一个可迭代对象(iterable)。该对象包含了spider用于爬取的第一个Request。
    # 当spider启动爬取并且未制定URL时，该方法被调用。 当指定了URL时，make_requests_from_url() 将被调用来创建Request对象。 该方法仅仅会被Scrapy调用一次，因此您可以将其实现为生成器。
    # 该方法的默认实现是使用 start_urls 的url生成Request。
    # 如果您想要修改最初爬取某个网站的Request对象，您可以重写(override)该方法。

    # 当response没有指定回调函数时，该方法是Scrapy处理下载的response的默认方法。
    def parse(self, response):
        for sel in response.xpath('//div[@class="mod-info-flow"]/div/div[@class="mob-ctt"]'):
            item = HuxiuItem()
            # 标题
            # title = sel.xpath('h2/a/text()').extract_first()
            # # 文章链接
            link = sel.xpath('h2/a/@href').extract_first()
            if link:
                next_url = response.urljoin(link)
                item['link'] = next_url
            # 简述
            desc = sel.xpath('div[@class="mob-sub"]/text()').extract_first()
            if next_url:
                request= scrapy.Request(next_url, callback=self.parse_article)
                request.meta['desc'] = desc
                yield request
            # yield 在每一次循环中相当于return ，只不过下次循环的时候，接着上一次进行循环，而不是从头开始循环

    def parse_article(self, response):
        desc=response.meta['desc']
        item = HuxiuItem()
        # 文章标题
        title = response.xpath('//div[@class="article-wrap"]/h1/text()').extract_first()
        # 文章作者
        author = response.xpath('//span[@class="author-name"]/a/text()').extract_first()
        # 文章发布时间
        post_time = response.xpath('//span[@class="article-time pull-left"]/text()').extract_first()
        # 文章头图链接
        pic_url = response.xpath('//div[@class="article-img-box"]/img/@src').extract_first()
        # 文章内容
        content = response.xpath('//div[@class="article-content-wrap"]/p/text()').extract()


        if title:
            item['title'] = title
        if author:
            item['author'] = author
        if post_time:
            item['post_time'] = post_time
        if pic_url:
            item['pic_url'] = pic_url
        if content:
            item['content'] = content
        item['desc'] = desc
        yield item




