# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter


class NSpiderPipeline:
    def __init__(self):
        self.f = open('it.json', 'a')

    def process_item(self, item, spider):
        self.f.write(str(item))
        return item

    def close_spider(self, spider):
        self.f.close()
