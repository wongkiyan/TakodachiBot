# Load configuration parameters
from pathlib import Path
from dotenv import load_dotenv
import os

# env setup
env_path = Path('.') / ".env"
load_dotenv(dotenv_path=env_path)

# App setting
APP_NAME = "Takodachi"
APP_TITLE = "Wah!"
APP_ICON_PATH = os.path.abspath("Takodachi_logo.png")

FOLDER_DISCORD_BAT_PATCH = "C:/Users/User/Documents/Discord/"
APP_STATUS_BAT_PATCH = os.path.join(FOLDER_DISCORD_BAT_PATCH,"TakodachiBot_Status.bat")

# Bot setting
BOT_DESCRIPTION = "A DD Takodachi"
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BOT_PREFIX = os.getenv("DISCORD_BOT_PREFIX", '!')

# Database setting
DATABASE_NAME = "data.db"

# Logger setting
LOG_DIRECTORY = 'logs'
LOGGER_CONFIGS_PATH = os.path.join(os.path.dirname(__file__),'library', 'logger.conf')

# region Archive module
# File patch
FOLDER_YT_DLP_BAT_PATCH                  = os.getenv("FOLDER_YT_DLP_BAT_PATCH")
ARCHIVE_YOUTUBE_STREAM_BAT_PATCH         = os.getenv("ARCHIVE_YOUTUBE_STREAM_BAT_PATCH")
ARCHIVE_VIDEO_BAT_PATCH                  = os.getenv("ARCHIVE_VIDEO_BAT_PATCH")

FOLDER_STREAMLINK_BAT_PATCH              = os.getenv("FOLDER_STREAMLINK_BAT_PATCH")
ARCHIVE_AND_PLAY_TWITCH_STREAM_BAT_PATCH = os.getenv("ARCHIVE_AND_PLAY_TWITCH_STREAM_BAT_PATCH")
ARCHIVE_TWITCH_STREAM_BAT_PATCH          = os.getenv("ARCHIVE_TWITCH_STREAM_BAT_PATCH")

# Archive command
ARCHIVE_YOUTUBE_LIVE_COMMAND             = os.getenv("ARCHIVE_YOUTUBE_LIVE_COMMAND")
ARCHIVE_TWITCH_LIVE_COMMAND              = os.getenv("ARCHIVE_TWITCH_LIVE_COMMAND")
ARCHIVE_VIDEO_COMMAND                    = os.getenv("ARCHIVE_VIDEO_COMMAND")
# endregion

# region Web scraper
WEB_HOLOLIVE_SCHEDULE = "https://schedule.hololive.tv/"

# endregion