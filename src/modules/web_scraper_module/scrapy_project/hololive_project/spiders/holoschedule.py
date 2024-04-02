from typing import Any, Iterable, Optional
from datetime import datetime
import re
import json
import pytz
from isodate import parse_duration

from scrapy import Spider, Request
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../../../../../..')))

from src.utils.datetime_utils import format_hk_datetime_by_string
from src.modules.web_scraper_module.scrapy_project.hololive_project.models import HoloSchedulesModel
from src.modules.web_scraper_module.scrapy_project.hololive_project.items import HoloSchedulesItem
from src.utils.database_utils import DatabaseUtils
from src.utils.google_utils import YoutubeAPIUtils, get_youtube_id_with_url
from src.modules.web_scraper_module.scrapy_project.hololive_project.constant import (
    api_json_path_mapping,
    response_xpath_mapping,
    live_content_state_mapping,
    VIDEO,
    LIVE,
    ON_ENDED,
    DATETIME_FORMAT
)

class DataExtractor():
    def __init__(self):
        self.schedule_data=None
        self.api_item_data=None

    def fill_schedule_data(self, item, schedule_data, stream_year, stream_date):
        self.schedule_data = schedule_data

        self.is_red_border = True if self.get_schedule_data('red_border') else False
        stream_time = self.get_schedule_data("time")
        collabs = self.get_schedule_data('collabs')
        short_name = self.get_schedule_data('short_name')

        item['stream_link'] = self.get_schedule_data('link')
        item['stream_id'] = get_youtube_id_with_url(item['stream_link'])
        item['stream_thumbnail'] = self.get_schedule_data('thumbnail')
        item['datetime_scheduled_start'] = format_datetime_for_web(stream_year, stream_date, stream_time)
        item['channel_short_name'] = " ".join(short_name) if isinstance(short_name, list) else short_name
        # item['channel_collabs'] = self.get_collabs_id(collabs)

        return item

    def fill_api_item_data(self, item, api_item_data):
        self.api_item_data = api_item_data

        item['stream_title'] = self.get_api_item_data('title')
        # item['stream_description'] = self.get_api_item_data('description')
        item['stream_duration'] = format_duration(self.get_api_item_data('duration')) # ("P0D" = on live)

        item['datetime_scheduled_start'] = format_datetime_for_api(self.get_api_item_data('scheduledStartTime')) or item['datetime_scheduled_start']
        item['datetime_actual_start'] = format_datetime_for_api(self.get_api_item_data('actualStartTime'))
        item['datetime_actual_end'] = format_datetime_for_api(self.get_api_item_data('actualEndTime'))

        item['stream_state'], item['stream_type'] = self.check_stream_state_type(item)

        item['channel_id'] = self.get_api_item_data('channel_id')
        item['channel_name'] = self.get_api_item_data('name')
        
        return item

    def get_schedule_data(self, key):
        return self.extract_text_with_xpath(self.schedule_data, key)
    
    def get_api_item_data(self, key):
        item = self.api_item_data
        paths = api_json_path_mapping.get(key, "").split('.')
        for path in paths:
            item = item.get(path, {})
        return item
    
    def check_stream_state_type(self, item):
        live_content = self.get_api_item_data('liveBroadcastContent') # ("none" = on ended, "live" = on live, "upcoming" = on scheduled)
        upload_status = self.get_api_item_data('uploadStatus') # ("processed" = on archived / on scheduled video, "uploaded" = on live / on scheduled live)

        stream_state = live_content_state_mapping.get(live_content, "UNKNOWN")

        if stream_state == ON_ENDED:
            if item['datetime_actual_start'] is None:
                stream_type = VIDEO
            else:
                stream_type = LIVE
        elif upload_status == "processed":
            stream_type = VIDEO
        elif upload_status == "uploaded":
            stream_type = LIVE
            
        return stream_state, stream_type
    
    def get_collabs_id(self, collabs):
        if isinstance(collabs, str):
            collabs = [collabs]
        return [re.search(r"/([a-zA-Z0-9_-]+)=s", url).group(1) for url in collabs]

    def extract_items_with_xpath(self, data, key):
        path = response_xpath_mapping.get(key)
        return data.xpath(path)

    def extract_text_with_xpath(self, data, key):
        path = response_xpath_mapping.get(key)
        items = data.xpath(path).re(r'\S+')
        if len(items) == 1:
            return items[0]
        return items

def format_datetime_for_web(year, date, time):
    return format_hk_datetime_by_string(f"{year}/{date} {time}", "%Y/%m/%d %H:%M").strftime(DATETIME_FORMAT)

def format_datetime_for_api(date_string):
    if date_string:
        return format_hk_datetime_by_string(date_string, "%Y-%m-%dT%H:%M:%SZ").strftime(DATETIME_FORMAT)
    return None

def format_duration(duration_str):
    duration = parse_duration(duration_str)

    days, seconds = divmod(duration.total_seconds(), 86400)
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if days:
        hours += int(days) * 24

    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def is_stream_id_in_database(stream_id):
    return database.query_model(HoloSchedulesModel, stream_id=stream_id) is not None

extractor = DataExtractor()
database = DatabaseUtils()
youtube_api = YoutubeAPIUtils()

class HoloScheduleSpider(Spider):
    name = "HoloSchedule"
    allowed_domains = ["schedule.hololive.tv", 'www.googleapis.com']
    start_urls = ["https://schedule.hololive.tv"]
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'src.modules.web_scraper_module.scrapy_project.hololive_project.middlewares.HoloScheduleDownloaderMiddleWare': 300
        },
    }

    def __init__(self, name: Optional[str] = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        self.item_callback = kwargs.get('item_callback', None)
        self.current_datetime = datetime.now(pytz.timezone('Asia/Hong_Kong'))
        self.previous_date = None
        self.data = None

    def start_requests(self) -> Iterable[Request]:
        # for url in self.start_urls:
        #     yield Request(url=url, callback=self.parse_schedule_data)
        file_path = 'file://C:/Users/User/Documents/Bot/TakodachiBot/src/modules/web_scraper_module/scrapy_project/hololive_project/spiders/test_data.html'
        yield Request(url=file_path, callback=self.parse_schedule_data)

    def parse_schedule_data(self, response):
        rows = extractor.extract_items_with_xpath(response, 'rows')

        for row in rows:
            date = extractor.extract_text_with_xpath(row, 'date') or self.previous_date
            self.previous_date = date if date else None

            schedules = extractor.extract_items_with_xpath(row, 'schedules')
            for schedule_data in schedules:
                item = HoloSchedulesItem()
                item = extractor.fill_schedule_data(item, schedule_data, self.current_datetime.year, date[0])

                url = youtube_api.get_youtube_videos_request_url(item['stream_id'])
                yield Request(url=url, callback=self.parse_youtube_data, meta={'item': item})

                # if not is_stream_id_in_database(item['stream_id']) or extractor.is_red_border:
                #     url = youtube_api.get_youtube_videos_request_url(
                #         item['stream_id'])
                #     yield Request(url=url, callback=self.parse_youtube_data, meta={'item': item})
                # else:
                #     yield item

    def parse_youtube_data(self, response):
        item = response.meta.get('item', {})
        if len(json.loads(response.text)['items']) > 0:
            api_data = json.loads(response.text)['items'][0]
            item = extractor.fill_api_item_data(item, api_data)
        yield item

if __name__ == '__main__':
    process = CrawlerProcess(
        settings={
            "ITEM_PIPELINES": {
                "src.modules.web_scraper_module.scrapy_project.hololive_project.pipelines.JSONPipeline": 300,
            },
        }
    )

    process.crawl(HoloScheduleSpider)
    process.start()

'''
custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        },
        'LOG_LEVEL': 'INFO',
        'LOG_FORMAT': '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        'LOG_DATEFORMAT': '%Y-%m-%d %H:%M:%S',
        'LOG_ENABLED': True,
        'LOG_STDOUT': True,
        'DOWNLOAD_DELAY': 3,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1,
        'AUTOTHROTTLE_START_DELAY': 5,
        'AUTOTHROTTLE_MAX_DELAY': 60,
        'AUTOTHROTTLE_DEBUG': False,
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'overwrite': True,
            },
        },
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_EXPORT_INDENT': 2,
        'FEED_EXPORTERS': {
            'json': 'scrapy.exporters.JsonItemExporter',
        },
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json',
        'IMAGES_STORE': 'images',
        'IMAGES_EXPIRES': 30,
        'IMAGES_MIN_HEIGHT': 110,
        'IMAGES_MIN_WIDTH': 110,
        'TELNETCONSOLE_PORT': [6023, 6073],
        'TELNETCONSOLE_HOST': '127.0.0.1',
        'TELNETCONSOLE_ENABLED': False,
        'CLOSESPIDER_TIMEOUT': 3600,
        'CLOSESPIDER_ITEMCOUNT': 100,
        'CLOSESPIDER_PAGECOUNT': 0,
        'CLOSESPIDER_ERRORCOUNT': 0,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': None,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': None,
            'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
            'TakodachiBot.src.middlewares.RotateUserAgentMiddleware': 543,
            'TakodachiBot.src.middlewares.RotateProxyMiddleware': 800,
        },
        'ITEM_PIPELINES': {
            'TakodachiBot.src.pipelines.CustomImagesPipeline': 1,
            'TakodachiBot.src.pipelines.JsonWriterPipeline': 2,
        },
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 503, 504, 400, 403, 404, 408],
        'ROBOTSTXT_OBEY': False,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        'TELNETCONSOLE_USERNAME': None,
        'TELNETCONSOLE_PASSWORD': None,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_TIMEOUT': 60,
        'REACTOR_THREADPOOL_MAXSIZE': 20,
        'FEED_EXPORT_FIELDS': ['schedule', 'stream', 'datetime', 'channel'],
        'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue',
        'REACTOR_THREADPOOL_MAXSIZE': 20,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
        'FEED_EXPORT_INDENT': 2,
        'FEED_EXPORT_ENCODING': 'utf-8',
        'TELNETCONSOLE_PORT': [6023, 6073],
        'TELNETCONSOLE_HOST': '127.0.0.1',
        'TELNETCONSOLE_ENABLED': False,
        'CLOSESPIDER_TIMEOUT': 3600,
        'CLOSESPIDER_ITEMCOUNT': 100,
        'CLOSESPIDER_PAGECOUNT': 0,
        'CLOSESPIDER_ERRORCOUNT': 0,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapy.downloadermiddlewares.redirect.MetaRefreshMiddleware': None,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': None,
            'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
            'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
            'TakodachiBot.src.middlewares.RotateUserAgentMiddleware': 543,
            'TakodachiBot.src.middlewares.RotateProxyMiddleware': 800,
        },
        'ITEM_PIPELINES': {
            'TakodachiBot.src.pipelines.CustomImagesPipeline': 1,
            'TakodachiBot.src.pipelines.JsonWriterPipeline': 2,
        },
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 503, 504, 400, 403, 404, 408],
        'ROBOTSTXT_OBEY': False,
        'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
        'TELNETCONSOLE_USERNAME': None,
        'TELNETCONSOLE_PASSWORD': None,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_TIMEOUT': 60,
        'REACTOR_THREADPOOL_MAXSIZE': 20,
        'FEED_EXPORT_FIELDS': ['schedule', 'stream', 'datetime', 'channel'],
        'SCHEDULER_PRIORITY_QUEUE': 'scrapy.pqueues.DownloaderAwarePriorityQueue',
        'REACTOR_THREADPOOL_MAXSIZE': 20,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
    }
'''