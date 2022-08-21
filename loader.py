import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config import Config
from utils.db_api.db import Database
from utils.db_api.users import Users
from utils.db_api.messages import Messages


# ChatBot objects
bot = Bot(token=Config.telegram_token, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
dp = Dispatcher(bot, storage=storage)

# Database objects
db = Database()
# Users from database
users = Users()
# Messages from database
messages = Messages()

# Logging setup
logging.basicConfig(handlers=(logging.FileHandler('logs/log.txt'), logging.StreamHandler()),
                    format=u'%(asctime)s %(filename)s [LINE:%(lineno)d] #%(levelname)-15s %(message)s',
                    level=logging.INFO,
                    )
