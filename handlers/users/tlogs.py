import logging
from aiogram.types import CallbackQuery

from filters import AdminCommand
from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=3600)
@dp.callback_query_handler(text="tlogs")
async def tlogs_tool(call: CallbackQuery):
    await dp.bot.send_document(call.from_user.id, document=open('troublelogs/tlogs.txt', 'rb'))
    await call.answer()
