from scrapy.cmdline import execute
from scrapy.crawler import CrawlerProcess
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
import multiprocessing

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(
        os.path.dirname(__file__), '../../..')))
    
from src.utils.datetime_utils import format_hk_datetime_by_string
from src.modules.web_scraper_module.scrapy_project.hololive_project.spiders.holoschedule import HoloScheduleSpider
from src.modules.web_scraper_module.scrapy_project.hololive_project.constant import (
    ON_ENDED,
    ON_LIVE,
    ON_SCHEDULED,
    DATETIME_FORMAT
)
from src.modules.scheduler_module.constants import JobType
from src.modules.archive_module.service import archive_youtube_stream

from configs import (
    SCHEDULER_HOLOLIVE_SCHEDULE_ID as HOLOLIVE_SCHEDULE_ID,
    LIST_HOLOLIVE_SUBSCRIBED_CHANNEL as SUBSCRIBED_CHANNEL,
    LIST_HOLOLIVE_SINGING_STREAM_KEYWORDS as SINGING_KEYWORDS,
    LIST_HOLOLIVE_SPECIAL_STREAM_KEYWORDS as SPECIAL_KEYWORDS,
    LIST_HOLOLIVE_UNARCHIVE_STREAM_KEYWORDS as UNARCHIVE_KEYWORDS,
    )

def start_scrapy(name):
    return execute(f"scrapy crawl {name}".split(" "))

class HololiveScheduleAPI():
    settings={
        "ITEM_PIPELINES": {
            "src.modules.web_scraper_module.scrapy_project.hololive_project.pipelines.SQLAlchemyPipeline": 200,
            "src.modules.web_scraper_module.scrapy_project.hololive_project.pipelines.JSONPipeline": 300,
            "src.modules.web_scraper_module.scrapy_project.hololive_project.pipelines.TakodachiPipeline": 300,
        },
    }

    def __init__(self, notify_methods=None, scheduler=None) -> None:
        super().__init__()
        self.notify_methods = notify_methods
        self.scheduler = scheduler

        self._ended = []
        self._live = []
        self._scheduled = []

        if self.scheduler:
            self.configure_scheduler()

    def configure_scheduler(self):
        self.scheduler.add_job(
            job_type = JobType.HOLOLIVE_TASK,
            job_id = HOLOLIVE_SCHEDULE_ID,
            job_func = self.run_crawler_api,
            trigger = CronTrigger(minute="1/15"),
            kwargs = {"jobstore": "memory"}
        )
    
    def run_crawler(self):
        process = CrawlerProcess(self.settings)
        process.crawl(HoloScheduleSpider, item_callback = self.item_callback)
        process.start()

    def run_crawler_api(self):
        crawler_process = multiprocessing.Process(target=self.run_crawler, args=(self,))
        crawler_process.start()
        crawler_process.join()

    def item_callback(self, item):
        stream_state = item.get("stream_state")
        stream_id = item.get("stream_id")
        channel_name = item.get("channel_name", "")
        stream_title = item.get("stream_title", "")
        scheduled_start_datetime = format_hk_datetime_by_string(item.get("datetime_scheduled_start"), DATETIME_FORMAT)
        
        old_stream_title = item.get("old_stream_title", None)
        old_scheduled_start_datetime = item.get("old_datetime_scheduled_start", None)

        if old_stream_title is not None and stream_title != old_stream_title:
            is_stream_title_updated = True
        else:
            is_stream_title_updated = False

        if old_scheduled_start_datetime is not None:
            is_scheduled_start_updated = scheduled_start_datetime != old_scheduled_start_datetime
        else:
            is_scheduled_start_updated = False

        if stream_state == ON_ENDED:
            self._ended.append(stream_id)
        elif stream_state == ON_LIVE:
            self._live.append(stream_id)
            self.notify(stream_title, channel_name)
            # if stream_title != old_item.get("stream_title"):
            #     self.notify(stream_title, f'「 {channel_name} 」更新了標題 \n old: {old_item.get("stream_title")}')
            # if stream_title != old_item.get("datetime_scheduled_start"):
            #     self.notify(stream_title, f'「 {channel_name} 」更新了標題 \n old: {old_item.get("stream_title")}')
        elif stream_state == ON_SCHEDULED:
            self._scheduled.append(stream_id)

            job = self.get_job(stream_id)

            is_subscribed_channel, is_singing_stream, is_special_stream, is_unarchive_stream, is_archiver_processed = self.check_statement(channel_name, stream_title, old_stream_title, is_stream_title_updated)
            
            if is_subscribed_channel or is_singing_stream or is_special_stream or is_unarchive_stream:
                if job is None:
                    self.add_notify_job(stream_id, stream_title, channel_name, scheduled_start_datetime)

            if is_unarchive_stream and is_archiver_processed is False:
                archive_youtube_stream(item.get("stream_link"))
        else:
            return

    def notify(self, stream_title, channel_name):
        if self.notify_methods is None:
            return
        
        title = f'「 {channel_name} 」 正在直播'
        message = stream_title

        for notify in self.notify_methods:
            notify(title, message)

    def get_job(self, job_id):
        return self.scheduler.get_job(job_id) if self.scheduler is not None else None
    
    def add_notify_job(self, stream_id, stream_title, channel_name, scheduled_start_datetime):
        if self.scheduler is None:
            return
        
        self.scheduler.add_job(
            job_type= JobType.HOLOLIVE_TASK,
            job_id= stream_id,
            trigger=DateTrigger(run_date=scheduled_start_datetime),
            job_func=self.notify,
            job_args=[stream_title, channel_name],
            job_kwargs=None)
        
    def resume_notify_job(self):
        if self.scheduler is None:
            return
        self.scheduler.resume_job(HOLOLIVE_SCHEDULE_ID)

    def pause_notify_job(self):
        if self.scheduler is None:
            return
        self.scheduler.pause_job(HOLOLIVE_SCHEDULE_ID)

    def check_statement(self, channel_name, title, old_title, is_stream_title_updated):
        is_subscribed_channel = channel_name in SUBSCRIBED_CHANNEL
        is_singing_stream = any(keyword.lower().replace(' ', '') in title.lower().replace(' ', '') for keyword in SINGING_KEYWORDS)
        is_special_stream = any(keyword.lower().replace(' ', '') in title.lower().replace(' ', '') for keyword in SPECIAL_KEYWORDS)
        is_unarchive_stream = any(keyword.lower().replace(' ', '') in title.lower().replace(' ', '') for keyword in UNARCHIVE_KEYWORDS)
        
        if is_unarchive_stream and is_stream_title_updated:
            is_old_stream_unarchive = any(keyword.lower().replace(' ', '') in old_title.lower().replace(' ', '') for keyword in UNARCHIVE_KEYWORDS)
            is_archiver_processed = is_old_stream_unarchive
        else:
            is_archiver_processed = False

        return is_subscribed_channel, is_singing_stream, is_special_stream, is_unarchive_stream, is_archiver_processed

if __name__ == "__main__":
    try:
        hololive_schedule_update_service = HololiveScheduleAPI()
        hololive_schedule_update_service.run_crawler()
        print()
        print("Ended    : " + str(len(hololive_schedule_update_service._ended)))
        print("Live     : " + str(len(hololive_schedule_update_service._live)))
        print("Scheduled: " + str(len(hololive_schedule_update_service._scheduled)))
    except Exception as e:
        print(f"錯誤: {e}")


'''
    stream_id
    stream_link
    stream_title
    stream_description
    stream_thumbnail
    stream_type
    stream_state
    stream_duration

    datetime_scheduled_start
    datetime_actual_start
    datetime_actual_end

    channel_id
    channel_name
    channel_short_name
    channel_collabs
'''