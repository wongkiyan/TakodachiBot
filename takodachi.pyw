#！ python3
import os
import asyncio
from threading import Thread
from pystray import Icon, Menu, MenuItem
from PIL import Image
import configs as Configs
import bot as DiscordBot
import subprocess

class App():
    def __init__(self):
        self.init_icon()

    def init_icon(self):
        twitch_submenu = Menu(
            MenuItem("Archive And Play",action=self.archive_and_play_twitch_stream_with_CMD),
            MenuItem("Archive Only",action=self.archive_twitch_stream_with_CMD),
        )
        app_menu = Menu(
            MenuItem("Archive Youtube Stream", action=self.archive_youtube_stream_with_cmd, default=True),
            MenuItem("Archive Twitch Stream...", twitch_submenu),
            MenuItem("Archive Video", action=self.archive_video_with_cmd),
            Menu.SEPARATOR,
            MenuItem("Show Logs", action=self.show_logs),
            MenuItem("Show Status", action=self.status),
            Menu.SEPARATOR,
            MenuItem("Exit", action=self.exit_application),
        )
        self.icon = Icon(name=Configs.APP_NAME, title=Configs.APP_TITLE, icon=Image.open(Configs.APP_ICON_PATH), menu=app_menu)

    def archive_youtube_stream_with_cmd(self):
        subprocess.Popen(['start', '', Configs.ARCHIVE_YOUTUBE_STREAM_PAT_PATCH], shell=True)

    def archive_and_play_twitch_stream_with_CMD(self):
        subprocess.Popen(['start', '', Configs.ARCHIVE_AND_PLAY_TWITCH_STREAM_PAT_PATCH], shell=True)

    def archive_twitch_stream_with_CMD(self):
        subprocess.Popen(['start', '', Configs.ARCHIVE_TWITCH_STREAM_PAT_PATCH], shell=True)

    def archive_video_with_cmd(self):
        subprocess.Popen(['start', '', Configs.ARCHIVE_VIDEO_BAT_PATCH], shell=True)

    def show_logs(self): 
        os.startfile("logs")

    def status(self):
        subprocess.Popen(['start', '', Configs.STATUS_PATCH], shell=True)

    def run(self):
        #self.start_discord_bot_thread()
        self.icon.run()

    def exit_application(self):
        #self.stop_discord_bot_thread()
        self.icon.visible = False
        self.icon.stop()
        os._exit(0)

    def start_discord_bot_thread(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(DiscordBot.client.start(Configs.BOT_TOKEN))
        self.t1=Thread(target=loop.run_forever)
        self.t1.start()

    def stop_discord_bot_thread(self):
        asyncio.get_event_loop().stop()
        if self.t1 is not None:
            self.t1.join()
        

if __name__ == "__main__":
    app = App()
    app.run()