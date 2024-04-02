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

FOLDER_PARENT_PATCH = os.path.join(base_folder_path, '../')
APP_PROCESS_NAME = "takodachi.pyw"
APP_STATUS_BAT_PATCH = os.path.join(FOLDER_PARENT_PATCH,"TakodachiBot_Status.bat")

# Service setting
SERVICE_APP_ICON = 'app_icon'
SERVICE_DISCORD_BOT = 'discord_bot'
SERVICE_VOLUME_CONTROL = 'volume_control'

SERVICE_SCHEDULER = 'scheduler'
SERVICE_HOLOLIVE_SCHEDULE = 'hololive_schedule'

# Database setting
DATABASE_NAME = "data/data.db"
DATABASE_MARIADB_USER = os.getenv("MARIADB_USER")
DATABASE_MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD")
DATABASE_MARIADB_HOST = os.getenv("MARIADB_HOST")
DATABASE_MARIADB_PORT = os.getenv("MARIADB_PORT")
DATABASE_MARIADB_NAME = os.getenv("MARIADB_NAME")
DATABASE_MARIADB_URL = f"mariadb+pymysql://{DATABASE_MARIADB_USER}:{quote_plus(DATABASE_MARIADB_PASSWORD)}@{DATABASE_MARIADB_HOST}:{DATABASE_MARIADB_PORT}/{DATABASE_MARIADB_NAME}"

# Logger setting
LOG_DIRECTORY = 'logs'
LOGGER_CONFIGS_PATH = os.path.join(os.path.dirname(__file__), 'src', 'library', 'logger.conf')

# API setting
API_YOUTUBE_KEY = os.getenv("YOUTUBE_API_KEY")

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

# region Discord Bot setting
BOT_DESCRIPTION = "A DD Takodachi"
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BOT_PREFIX = os.getenv("DISCORD_BOT_PREFIX", '!')

DISCORD_EXCEPTION_CHANNEL_ID = 1185820334146981958
# endregion

# region Hololive Schedule
SCHEDULER_HOLOLIVE_SCHEDULE_ID = "hololive_schedule_data_update"

WEB_HOLOLIVE_SCHEDULE = "https://schedule.hololive.tv/"

LIST_HOLOLIVE_SUBSCRIBED_CHANNEL = []
LIST_HOLOLIVE_SINGING_STREAM_KEYWORDS = ['karaoke', 'sing', 'uta', '歌', 'カラオケ']
LIST_HOLOLIVE_SPECIAL_STREAM_KEYWORDS = ['3D Live', '周年LIVE', '周年記念LIVE', '生誕祭', '3D CONCERT']
LIST_HOLOLIVE_UNARCHIVE_STREAM_KEYWORDS = ['unarchived', 'unarchive', 'no archive']
# endregion