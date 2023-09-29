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
ARCHIVE_YOUTUBE_STREAM_PAT_PATCH = "C:/Users/User/Documents/VtuberDownloadTools/yt-dlp/yt-dlp_ArchiveYoutubeStream.bat"
ARCHIVE_VIDEO_BAT_PATCH          = "C:/Users/User/Documents/VtuberDownloadTools/yt-dlp/yt-dlp_ArchiveYoutubeVideoWithAria2.bat"

ARCHIVE_ADVANCED_TWITCH_STREAM_PAT_PATCH = "C:/Users/User/Documents/VtuberDownloadTools/streamlink/streamlink_ArchiveAdvanced.bat"
ARCHIVE_AND_PLAY_TWITCH_STREAM_PAT_PATCH = "C:/Users/User/Documents/VtuberDownloadTools/streamlink/streamlink_ArchiveWithPlay.bat"
ARCHIVE_TWITCH_STREAM_PAT_PATCH          = "C:/Users/User/Documents/VtuberDownloadTools/streamlink/streamlink_ArchiveWithoutPlay.bat"

STATUS_PATCH = "C:/Users/User/Documents/Discord/TakodachiBot_Status.bat"