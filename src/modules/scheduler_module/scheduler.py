from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from tzlocal import get_localzone
from logging import getLogger

import configs

preset_jobstores = {
    'default': SQLAlchemyJobStore(url=configs.DATABASE_MARIADB_URL),
    'memory': MemoryJobStore()
}

preset_executors = {
    'default': ThreadPoolExecutor(100),
    'processpool': ProcessPoolExecutor(5)
}

preset_job_defaults = {
    'coalesce': False,
    'max_instances': 3,
    'misfire_grace_time': 900,
    'trigger': 'cron',
    'replace_existing': False
}

def ensure_dict(param, preset_dict):
    if param is None:
        return preset_dict
    if not isinstance(param, dict):
        return {'default': param}
    return param

class Scheduler(BackgroundScheduler):
    def __init__(self, logger=None, daemon=None, timezone=None):
        jobstores = preset_jobstores
        executors = preset_executors
        job_defaults = preset_job_defaults
        timezone = timezone or get_localzone()
        logger = logger or getLogger('scheduler')
        daemon = daemon or True
        super().__init__(jobstores=jobstores, executors=executors, job_defaults=job_defaults, logger=logger, daemon=daemon, timezone=timezone)