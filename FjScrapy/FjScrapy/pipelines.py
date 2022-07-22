# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


# class FjscrapyPipeline:
#     def process_item(self, item, spider):
#         return item

class MongoPipeline:
    def open_spider(self, spider):
        self.client = MongoClient()
        self.collection = self.client.ScrapyCollcetion.lianjia

    def process_item(self, item, spider):   # 这里踩了位置参数的坑
        self.collection.insert_one(item)    # 插入数据
        return item

    def close_spider(self, spider):
        self.client.close()     # 使用完数据库记得关闭
