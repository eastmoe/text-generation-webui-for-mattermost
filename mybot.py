#!/usr/bin/env python

from mmpy_bot import Bot, Settings
from chat import TestPlugin

bot = Bot(
    settings=Settings(
        MATTERMOST_URL = "http://192.168.31.184",
        MATTERMOST_PORT = 8065,
        MATTERMOST_API_PATH = '/api/v4',
        BOT_TOKEN = "cbgherhcnif38kxabz5d638agh",
        BOT_TEAM = "room",
        SSL_VERIFY = False,
    ),  # Either specify your settings here or as environment variables.
    plugins=[ChatPlugin()],  # Add your own plugins here.
)
bot.run()
