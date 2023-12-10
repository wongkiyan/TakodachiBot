import time
from datetime import date

from src.modules.base_service import BaseService
from src.modules.scheduler_module.scheduler import Scheduler

class TimingNotifyService(BaseService):
    def __init__(self):
        super().__init__()
        self.scheduler = Scheduler(timezone="Asia/Hong_Kong")
        self._schedule_timing_notifies = []

    def start_service(self):
        super().start_service()
        self.scheduler.start()

    def stop_service(self):
        super().stop_service()
        self.scheduler.shutdown()

    def is_running(self):
        return super().is_running()
    

if __name__ == "__main__":
    service = TimingNotifyService()
    service.start_service()

    start_time_tomorrow = time.strftime("%Y-%m-%d") + " 00:00:00"
    service.add_job(
        my_job, 'date', run_date=date(2009, 11, 6), args=['text'])
    service.add_job(my_job, 'date', days=1, args=['text'])
