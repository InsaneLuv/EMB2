import logging

from aiogram.utils import executor

from background import keep_alive
from utils.multilanguage import setup_multilanguage

LOG_LEVEL = logging.INFO

from colorlog import ColoredFormatter

logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(
  logging.basicConfig(
                      format='%(asctime)s | %(message)s',
                      datefmt='%H:%M',
                      level=logging.INFO))
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger()
log.setLevel(LOG_LEVEL)
log.addHandler(stream)

async def on_startup(dp):
  from utils.notify_admins import on_startup_notify
  await on_startup_notify(dp)

  import filters
  filters.setup(dp)

  import middlewares
  middlewares.setup(dp)

  from utils.set_bot_commands import set_default_commands
  await set_default_commands(dp)

  from database import sqlite_db
  await sqlite_db.sql_start()


async def on_shutdown(dp):
  logging.warning('Shutting down..')
  # await bot.delete_webhook()
  await dp.storage.close()
  await dp.storage.wait_closed()

  logging.warning('Bye!')


if __name__ == "__main__":

  from handlers import dp
  keep_alive()
  executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown,skip_updates=True)

