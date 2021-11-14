from db import Database
from parser import EdupageNewsParser
import config
from apscheduler.schedulers.blocking import BlockingScheduler

database = Database()
parser = EdupageNewsParser(config.DISCORD_WEBHOOK_URL, config.WEBSITE_URL, database)


def check():
    print("Checking for news...")
    parser.get_all_news()


check()


scheduler = BlockingScheduler(timezone="Europe/Bratislava")
scheduler.add_job(check, 'interval', minutes=1)
scheduler.start()
