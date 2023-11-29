#！ python3
import os
import asyncio
from threading import Thread
from pystray import Icon, Menu, MenuItem
from PIL import Image
import configs as Configs
import subprocess
from tkinter import messagebox as Messagebox
from logging.config import fileConfig
from concurrent.futures import ThreadPoolExecutor
from modules.discord_bot_module import DiscordBotService
from modules.volume_control_module import VolumeControlService
from library.managers.environment_manager import EnvironmentManager

class App():
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.executor = ThreadPoolExecutor()
        self.services = {}
        self.discord_bot_service = DiscordBotService()
        self.volume_control_service = VolumeControlService()
        self.init_logger()
        self.init_icon()

    def init_logger(self):
        if not os.path.exists(Configs.LOG_DIRECTORY):
            os.makedirs(Configs.LOG_DIRECTORY)
        fileConfig(Configs.LOGGER_CONFIGS_PATH, disable_existing_loggers=False, encoding="utf-8")

    def init_icon(self):  # Taskbar
        twitch_submenu = Menu(
            MenuItem("Archive And Play", self.archive_and_play_twitch_stream_with_CMD),
            MenuItem("Archive Only", self.archive_twitch_stream_with_CMD),
        )
        volume_submenu = Menu(
            MenuItem("Start Limit Volume", self.start_volume_control_service),
            MenuItem("Stop Limit Volume", self.stop_volume_control_service),
        )
        app_menu = Menu(
            MenuItem("Archive Youtube Stream",  self.archive_youtube_stream_with_CMD, default = True),
            MenuItem("Archive Twitch Stream...", twitch_submenu),
            MenuItem("Archive Video", self.archive_video_with_CMD),
            Menu.SEPARATOR,
            MenuItem("App Logs", self.show_logs),
            MenuItem("App Status", self.show_app_status),
            MenuItem("Discord Status", self.show_discord_status),
            Menu.SEPARATOR,
            MenuItem("Volume Control",volume_submenu),
            Menu.SEPARATOR,
            MenuItem("Exit", action=self.exit),
        )
        self.icon = Icon(name=Configs.APP_NAME, title=Configs.APP_TITLE, icon=Image.open(Configs.APP_ICON_PATH), menu=app_menu)

    def archive_youtube_stream_with_CMD(self):
        process = subprocess.Popen(['start', '', Configs.ARCHIVE_YOUTUBE_STREAM_BAT_PATCH], shell=True)
        # self.add_process(process)

    def archive_and_play_twitch_stream_with_CMD(self):
        process = subprocess.Popen(['start', '', Configs.ARCHIVE_AND_PLAY_TWITCH_STREAM_BAT_PATCH], shell=True)
        # self.add_process(process)

    def archive_twitch_stream_with_CMD(self):
        process = subprocess.Popen(['start', '', Configs.ARCHIVE_TWITCH_STREAM_BAT_PATCH], shell=True)
        # self.add_process(process)

    def archive_video_with_CMD(self):
        process = subprocess.Popen(['start', '', Configs.ARCHIVE_VIDEO_BAT_PATCH], shell=True)
        # self.add_process(process)

    def show_logs(self):
        os.startfile("logs")

    def show_app_status(self):
        subprocess.Popen(['start', '', Configs.APP_STATUS_BAT_PATCH], shell=True)

    def show_discord_status(self):
        if self.discord_bot_service.is_running():
            return self.notify("Discord Bot is ready!" ) 
        return self.notify("Discord Bot is closed!" )

    def notify(self, notify_message):
        self.icon.notify(
            title='Takodachi says',
            message=notify_message,)

    def run(self):
        self.start_discord_bot_service()
        self.icon.run()

    def exit(self):
        if self.discord_bot_service.is_running():
            self.stop_discord_bot_service()
        if self.volume_control_service.is_running():
            self.stop_volume_control_service()
        self.icon.visible = False
        self.icon.stop()
        os._exit(0)

    def start_discord_bot_service(self):
        self.loop.run_in_executor(self.executor, self.discord_bot_service.start_service)

    def stop_discord_bot_service(self):
        if self.discord_bot_service.is_running():
            self.loop.run_in_executor(self.executor, self.discord_bot_service.stop_service)

    def start_volume_control_service(self):
        if not EnvironmentManager.is_admin():
            return self.notify("This script requires administrative privileges to modify audio settings.")
        self.loop.run_in_executor(self.executor, self.volume_control_service.start_service)

    def stop_volume_control_service(self):
        if not EnvironmentManager.is_admin():
            return self.notify("This script requires administrative privileges to modify audio settings.")
        self.loop.run_in_executor(self.executor, self.volume_control_service.stop_service)

if __name__ == "__main__":
    app = App()
    app.run()