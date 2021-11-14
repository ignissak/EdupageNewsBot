import os

from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
