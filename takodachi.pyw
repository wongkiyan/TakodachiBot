#！ python3
import os
import asyncio

from logging.config import fileConfig, dictConfig
from src.library.logger_dict_config import logging_config

import configs

from src.modules import ServicesManager

class App():
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.services_manager = ServicesManager(loop=self.loop, exit_callback = self.exit)
        self.init_logger()

    def init_logger(self):
        if not os.path.exists(configs.LOG_DIRECTORY):
            os.makedirs(configs.LOG_DIRECTORY)

        if os.path.exists(configs.LOGGER_CONFIGS_PATH):
            fileConfig(configs.LOGGER_CONFIGS_PATH, disable_existing_loggers=False, encoding="utf-8")
        else:
            dictConfig(logging_config)

    def run(self):
        self.services_manager.start_default_service()
        self.loop.run_forever()

    def exit(self):
        self.services_manager.stop_all_services()
        self.loop.stop()

if __name__ == "__main__":
    app = App()
    app.run()