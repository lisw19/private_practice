import scrapy

from n_spider.items import NSpiderItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['baidu.com']
    start_urls = ['https://www.baidu.com/']

    def parse(self, response):
        print(response.body)
        items = response.xpath('//a')
        item = NSpiderItem()

        for it in items:
            href = it.xpath("./@href")
            item['name'] = href
            yield item
