from envparse import Env

env = Env()
env.read_envfile()

DISCORD_WEBHOOK_URL = env("DISCORD_WEBHOOK_URL")
SQLITE_DATABASE_URL = env("SQLITE_DATABASE_URL")
WEBSITE_URL = env("WEBSITE_URL")