import os
import re
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Ensure DEBUG is correctly interpreted as a boolean
DEBUG = os.getenv("DEBUG", "False").strip().lower() in ("1", "true", "yes", "on")

# Define directories based on DEBUG mode
DOWNLOAD_DIRECTORY = "downloads" if DEBUG else os.path.join(os.path.expanduser("~"), "Music")
CACHE_DIRECTORY = "cache"
OUTPUT_FORMATS = {'audio': 'mp3', 'video': 'mp4'}
MAX_CONCURRENT_DOWNLOADS = 3
COMPLETION_SOUND_FREQ = 1000
COMPLETION_SOUND_DURATION = 500

# Create necessary directories
os.makedirs(DOWNLOAD_DIRECTORY, exist_ok=True)
os.makedirs(CACHE_DIRECTORY, exist_ok=True)

# Regex for detecting YouTube videos
YOUTUBE_VIDEO_REGEX = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.?be/)[\w-]{11}$'
