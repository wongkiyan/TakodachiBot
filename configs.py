# Load configuration parameters
from pathlib import Path
from dotenv import load_dotenv
import os

# env setup
env_path = Path('.') / ".env"
load_dotenv(dotenv_path=env_path)

# Bot setting
BOT_DESCRIPTION = "A DD Takodachi"
BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
BOT_PREFIX = os.getenv("DISCORD_BOT_PREFIX", '!')

# App setting
APP_NAME = "Takodachi"
APP_TITLE = "Wah!"
APP_ICON_PATH = os.path.abspath("Takodachi_logo.png")

# Path setting
ARCHIVE_YOUTUBE_STREAM_BAT_PATCH             = "C:/Users/User/Documents/VtuberDownloadTools/yt-dlp/yt-dlp_ArchiveYoutubeStream.bat"

ARCHIVE_VIDEO_BAT_PATCH                      = "C:/Users/User/Documents/VtuberDownloadTools/yt-dlp/yt-dlp_ArchiveYoutubeVideoWithAria2.bat"
ARCHIVE_VIDEO_NO_PROGRESS_BAT_PATCH          = "C:/Users/User/Documents/VtuberDownloadTools/yt-dlp/yt-dlp_ArchiveYoutubeVideoWithAria2_NoProgress.bat"

ARCHIVE_AND_PLAY_TWITCH_STREAM_BAT_PATCH     = "C:/Users/User/Documents/VtuberDownloadTools/streamlink/streamlink_ArchiveWithPlay.bat"

ARCHIVE_TWITCH_STREAM_BAT_PATCH              = "C:/Users/User/Documents/VtuberDownloadTools/streamlink/streamlink_ArchiveWithoutPlay.bat"
ARCHIVE_TWITCH_STREAM_NO_PROGRESS_BAT_PATCH  = "C:/Users/User/Documents/VtuberDownloadTools/streamlink/streamlink_ArchiveWithoutPlay_NoProgress.bat"

STATUS_PATCH = "C:/Users/User/Documents/Discord/TakodachiBot_Status.bat"

# Archive command
ARCHIVE_YOUTUBE_LIVE_COMMAND = "yt-dlp --no-progress"
ARCHIVE_TWITCH_LIVE_COMMAND = "streamlink --progress no --output C:/Users/User/Videos/Vtuber/{author}/{time:%Y%m%d}_{category}_{title}.ts"
ARCHIVE_VIDEO_COMMAND = 'yt-dlp --no-progress --external-downloader aria2c --downloader-args aria2c:"-x 8 -k 1M"'

# Logger setting
LOG_DIRECTORY = 'logs'
LOGGER_CONFIGS_PATH = os.path.join(os.path.dirname(__file__),'library', 'logger.conf')