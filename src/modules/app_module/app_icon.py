import subprocess
from pystray import Icon, Menu, MenuItem
from PIL import Image
import os
import configs

class AppIcon(Icon):
    def __init__(self, services_manager, exit_callback):
        self.services_manager = services_manager
        self.exit_callback = exit_callback
        self.notify_title = "Takodachi says"
        super().__init__(name=configs.APP_NAME, title=configs.APP_TITLE, icon=Image.open(configs.APP_ICON_PATH), menu=self.init_menu())

    def init_menu(self):
        twitch_submenu = Menu(
            MenuItem("Archive And Play", self.archive_and_play_twitch_stream_with_CMD),
            MenuItem("Archive Only", self.archive_twitch_stream_with_CMD),
        )
        volume_submenu = Menu(
            MenuItem("Start Limit Volume", self.start_volume_control),
            MenuItem("Stop Limit Volume", self.stop_volume_control),
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
        return app_menu

    def archive_youtube_stream_with_CMD(self):
        subprocess.Popen(['start', '', configs.ARCHIVE_YOUTUBE_STREAM_BAT_PATCH], shell=True)

    def archive_and_play_twitch_stream_with_CMD(self):
        subprocess.Popen(['start', '', configs.ARCHIVE_AND_PLAY_TWITCH_STREAM_BAT_PATCH], shell=True)

    def archive_twitch_stream_with_CMD(self):
        subprocess.Popen(['start', '', configs.ARCHIVE_TWITCH_STREAM_BAT_PATCH], shell=True)

    def archive_video_with_CMD(self):
        subprocess.Popen(['start', '', configs.ARCHIVE_VIDEO_BAT_PATCH], shell=True)

    def show_logs(self):
        os.startfile("logs")

    def show_notify(self, notify_message):
        self.notify(
            title=self.notify_title,
            message=notify_message)

    def show_app_status(self):
        subprocess.Popen(['start', configs.APP_STATUS_BAT_PATCH], shell=True)

    def show_discord_status(self):
        if self.services_manager.is_service_running(configs.SERVICE_DISCORD_BOT):
            return self.show_notify("Discord Bot is running!")
        return self.show_notify("Discord Bot is stopped!")

    def start_volume_control(self):
        self.services_manager.start_service(configs.SERVICE_VOLUME_CONTROL)

    def stop_volume_control(self):
        self.services_manager.stop_service(configs.SERVICE_VOLUME_CONTROL)

    def exit(self):
        self.exit_callback()