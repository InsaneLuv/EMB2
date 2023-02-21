from aiogram import types

from filters import IsSubscriber
from keyboards.inline import help_ikb_menu
from loader import dp, _


@dp.message_handler(IsSubscriber(),lambda message: "🛎" in message.text)
async def show_inline_menu(message: types.Message):
    await message.reply(_('🛎 Тебе нужна помощь? Выбери чего ты хочешь.'), reply_markup=help_ikb_menu)
