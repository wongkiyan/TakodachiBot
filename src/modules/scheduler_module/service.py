from logging import getLogger
from logging import DEBUG, INFO, WARN, ERROR, FATAL

from src.modules.scheduler_module.scheduler import Scheduler
from src.modules.scheduler_module.constants import JobType, INIT_JOBS_CONFIG
from src.modules.base_service import BaseService

class SchedulerService(BaseService):
    def __init__(self):
        super().__init__()
        logger = getLogger('apscheduler').setLevel(WARN)
        daemon = None
        timezone = "Asia/Hong_Kong"
        self.scheduler = Scheduler(logger=logger, daemon=daemon, timezone=timezone)
        self.jobs = {job_type: [] for job_type in JobType.get_all_types()}
        self.init_jobs()

    def init_jobs(self):
        for config in INIT_JOBS_CONFIG:
            self.remove_job(config["job_id"])
            self.add_job(config["job_type"], config["job_id"], config["trigger"], config["job_func"], config["job_args"], config["job_kwargs"], config["kwargs"])

    def get_job(self, job_id):
        return self.scheduler.get_job(job_id)

    def reschedule_job(self, job_id, trigger, kwargs):
        self.scheduler.reschedule_job(job_id, trigger=trigger, **kwargs)

    def add_job(self, job_type, job_id, trigger, job_func, job_args=None, job_kwargs=None, kwargs=None):
        if kwargs is None:
            kwargs = {}
        job = self.scheduler.add_job(id=job_id, trigger=trigger, func=job_func, args=job_args, kwargs=job_kwargs, **kwargs)
        self.jobs[job_type].append(job)
        return job

    def remove_job(self, job_id):
        if self.get_job(job_id):
            self.scheduler.remove_job(job_id)

    def pause_job(self, job_id):
        self.scheduler.pause_job(job_id)

    def resume_job(self, job_id):
        self.scheduler.resume_job(job_id)

    def pause_jobs_by_type(self, job_type):
        for job in self.jobs[job_type]:
            job.pause()

    def resume_jobs_by_type(self, job_type):
        for job in self.jobs[job_type]:
            job.resume()

    def start_service(self):
        super().start_service()
        self.scheduler.start()

    def stop_service(self):
        super().stop_service()
        self.scheduler.shutdown()

    def pause_service(self):
        self.scheduler.pause()

    def resume_service(self):
        self.scheduler.resume()

    def is_running(self):
        return super().is_running()

if __name__ == "__main__":
    scheduler_service = SchedulerService()
    try:
        scheduler_service.start_service()
        while True:
            pass
    except KeyboardInterrupt:
        pass
    finally:
        scheduler_service.stop_service()