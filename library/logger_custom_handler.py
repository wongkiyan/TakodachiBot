import logging
import configs as Configs
import os
from datetime import datetime

class DynamicFileHandler(logging.FileHandler):
    def __init__(self, log_type="", mode='a', encoding=None, delay=False):
        filename = os.path.join(Configs.LOG_DIRECTORY, log_type, self.get_current_date() + '.log')
        os.makedirs(os.path.join(Configs.LOG_DIRECTORY, log_type), exist_ok=True)
        super().__init__(filename, mode, encoding, delay)

    def get_current_date(self):
        return datetime.now().strftime('%Y-%m-%d')