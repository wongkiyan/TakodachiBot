# Declare top-level shortcuts
from .base_service import BaseService

from .app_module.service import AppIconService
from .scheduler_module.service import SchedulerService
from .hololive_schedule_module.api import HololiveScheduleAPI

from .discord_bot_module.service import DiscordBotService
from .volume_control_module.service import VolumeControlService

from .services_manager import ServicesManager

__all__=[
    "ServicesManager",
    "BaseService",
    "AppIconService",
    "SchedulerService",
    "HololiveScheduleAPI",
    "DiscordBotService",
    "VolumeControlService",
]