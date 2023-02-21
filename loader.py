
import os

from aiogram import Bot
from aiogram import types
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

from utils.multilanguage import setup_multilanguage

load_dotenv()

BOT_TOKEN = os.getenv("token")

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

dp = Dispatcher(bot, storage=storage)

i18n = setup_multilanguage(dp)
_ = i18n.gettext
__ = i18n.lazy_gettext
