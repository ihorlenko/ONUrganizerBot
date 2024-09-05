import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
SCHEDULE_IMAGE_PATH = os.path.join(os.path.dirname(__file__), '../data/schedule.jpg')
