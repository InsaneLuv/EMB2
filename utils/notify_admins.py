from aiogram import Dispatcher

from data.config import admins, technical_messages


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(chat_id=admin, text=technical_messages['bot_start'], disable_notification=True)
        except Exception as err:
            pass