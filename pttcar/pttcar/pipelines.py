# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


from pymongo import MongoClient
from scrapy.utils.project import get_project_settings

class PttcarPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):  # 處裡讀回來的項目
        self.collection.insert(dict(item))  # 用dictionary轉換json格式在insert到collection裡面
        return item




