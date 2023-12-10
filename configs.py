# Load configuration parameters
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

base_folder_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))

# env setup
# env_path = Path('.') / ".env"
env_path = os.path.join(base_folder_path, '.env')
load_dotenv(dotenv_path=env_path)

# App setting
APP_NAME = "Takodachi"
APP_TITLE = "Wah!"
APP_ICON_PATH = os.path.join(base_folder_path, './assets/icon_logo.png')

FOLDER_DISCORD_BAT_PATCH = "C:/Users/User/Documents/Discord/"

APP_PROCESS_NAME = "takodachi.pyw"
APP_STATUS_BAT_PATCH = os.path.join(FOLDER_DISCORD_BAT_PATCH,"TakodachiBot_Status.bat")

# Service setting
SERVICE_APP_ICON = 'app_icon'
SERVICE_DISCORD_BOT = 'discord_bot'
SERVICE_VOLUME_CONTROL = 'volume_control'

# Bot setting
BOT_DESCRIPTION = "A DD Takodachi"
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BOT_PREFIX = os.getenv("DISCORD_BOT_PREFIX", '!')

# Database setting
DATABASE_NAME = "data/data.db"
DATABASE_MARIADB_USER = os.getenv("MARIADB_USER")
DATABASE_MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD")
DATABASE_MARIADB_HOST = os.getenv("MARIADB_HOST")
DATABASE_MARIADB_PORT = os.getenv("MARIADB_PORT")
DATABASE_MARIADB_NAME = os.getenv("MARIADB_NAME")
DATABASE_MARIADB_URL = f"mariadb+pymysql://{DATABASE_MARIADB_USER}:{
    quote_plus(DATABASE_MARIADB_PASSWORD)}@{DATABASE_MARIADB_HOST}:{DATABASE_MARIADB_PORT}/{DATABASE_MARIADB_NAME}"

# Logger setting
LOG_DIRECTORY = 'logs'
LOGGER_CONFIGS_PATH = os.path.join(os.path.dirname(__file__), 'src', 'library', 'logger.conf')

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

# region Hololive Schedule
WEB_HOLOLIVE_SCHEDULE = "https://schedule.hololive.tv/"

LIST_HOLOLIVE_SINGING_STREAM_KEYWORDS = ['karaoke','sing', 'uta', '歌', 'カラオケ']
# endregion