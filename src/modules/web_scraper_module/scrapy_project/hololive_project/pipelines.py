# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.signalmanager import dispatcher
from datetime import datetime
import json

from .signals import schedule_data_updated
from .....utils.database_utils import DatabaseUtils
from .models import HoloSchedulesModel
from .helper import convert_item
from .items import (
    HoloSchedulesJSONItem,
    HoloSchedulesDatabaseItem
)

class JSONPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w', encoding='utf-8')
        self.file.truncate()
        self.file.write("[\n")

    def process_item(self, item, spider):
        json_item = convert_item(HoloSchedulesJSONItem, item)
        try:
            self.file.write(json.dumps(dict(json_item), ensure_ascii=False, default=self.custom_json_encoder) + ",\n")
        except BaseException as e:
            print(e)
        return item

    def close_spider(self, spider):
        self.file.seek(self.file.tell() - 3, 0)
        self.file.truncate()
        self.file.write("\n]")
        self.file.close()

    def custom_json_encoder(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # 將 datetime 對象轉換為 ISO 格式字符串
        raise TypeError("Type not serializable")

class SQLAlchemyPipeline:
    def __init__(self, database_url=None):
        self.database = DatabaseUtils(database_url)

    @classmethod
    def from_crawler(cls, crawler):
        database_url = crawler.settings.get('DATABASE_MARIADB_URL')
        return cls(database_url)

    def process_item(self, item, spider):
        database_item = convert_item(HoloSchedulesDatabaseItem, item)
        data_model = HoloSchedulesModel(**database_item)

        old_item = self.database.query_model(HoloSchedulesModel, stream_id=item.get("stream_id"))
        if old_item is not None:
            database_item['old_stream_title'] = old_item.stream_title
            database_item['old_datetime_scheduled_start'] = old_item.datetime_scheduled_start
        
        self.database.execute_data_model(data_model)
        return item
    
class TakodachiPipeline:
    def process_item(self, item, spider):
        if hasattr(spider, 'item_callback') and callable(spider.item_callback):
            spider.item_callback(item)
        return item


