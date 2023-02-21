import logging
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data.config import chat_ids
from loader import bot, dp, _
from data.config import admins

class AdminCommand(BoundFilter):
    async def check(self, message: types.Message):
        if message.from_user.id in admins:
            return True
        else:
            logging.info(f"User {message.from_user.id} is not an admin")
            return False