from aiogram import types

from filters import IsSubscriber
from keyboards.inline import tools_ikb_menu
from loader import dp,_
from utils.misc import rate_limit


@rate_limit(limit=2)
@dp.message_handler(IsSubscriber(),lambda message: "⚒" in message.text)
async def button_rules_react(message: types.Message):
    await message.reply(_('🛠 Выбери инструмент:'),reply_markup=tools_ikb_menu)