from apscheduler.triggers.cron import CronTrigger

class JobType:
    APP_TASK = 'App task'
    HOLOLIVE_TASK = 'Hololive task'

    @classmethod
    def get_all_types(cls):
        return [value for name, value in vars(cls).items() if not name.startswith("__")]

def test_func():
    print("test")

INIT_JOBS_CONFIG = [
    # {   "job_type": JobType.APP_TASK,
    #     "job_id": "clear_log_file",
    #     "job_func": test_func,
    #     "job_args":[],
    #     "job_kwargs": {},
    #     "trigger": CronTrigger(day='*'),
    #     "kwargs": {"jobstore": "memory"}},

    # {   "job_type": JobType.APP_TASK,
    #     "job_id": "test",
    #     "job_func": test_func,
    #     "job_args": [],
    #     "job_kwargs": {},
    #     "trigger": CronTrigger(second='*'),
    #     "kwargs": {"jobstore": "memory"}},
]