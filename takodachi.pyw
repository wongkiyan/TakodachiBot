#！ python3
import os
import asyncio

from concurrent.futures import ThreadPoolExecutor
from logging.config import fileConfig

import configs

from src.managers.services_manager import ServicesManager

class App():
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.executor = ThreadPoolExecutor()
        self.services_manager = ServicesManager(loop=self.loop, executor=self.executor, exit_callback = self.exit)
        self.init_logger()

    def init_logger(self):
        if not os.path.exists(configs.LOG_DIRECTORY):
            os.makedirs(configs.LOG_DIRECTORY)
        fileConfig(configs.LOGGER_CONFIGS_PATH, disable_existing_loggers=False, encoding="utf-8")

    def run(self):
        self.services_manager.start_service(configs.SERVICE_DISCORD_BOT)
        self.services_manager.start_service(configs.SERVICE_APP_ICON)
        self.loop.run_forever()

    def exit(self):
        self.services_manager.stop_all_services()
        self.loop.stop()

if __name__ == "__main__":
    app = App()
    app.run()