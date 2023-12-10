from collections import OrderedDict
import configs

from src.modules import DiscordBotService
from src.modules import VolumeControlService
from src.modules import AppIconService

class ServicesManager():
    def __init__(self, loop, executor, exit_callback):
        self.loop = loop
        self.executor = executor
        self.exit_callback = exit_callback
        self.services = OrderedDict()
        self.init_services()

    def init_services(self):
        self.services[configs.SERVICE_DISCORD_BOT] = DiscordBotService()
        self.services[configs.SERVICE_VOLUME_CONTROL] = VolumeControlService()
        self.services[configs.SERVICE_APP_ICON] = AppIconService(self, self.exit_callback)

    def start_service(self, service_name):
        service = self.services.get(service_name, None)
        if service:
            self.loop.run_in_executor(self.executor, service.start_service)

    def stop_service(self, service_name):
        service = self.services.get(service_name, None)
        if service:
            self.loop.run_in_executor(self.executor, service.stop_service)

    def stop_all_services(self):
        for service in self.services.values():
            service.stop_service()

    def is_service_running(self, service_name):
        service = self.services.get(service_name, None)
        if service:
            return service.is_running()