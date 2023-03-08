from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data.config import admins
from database import profile_reg, lang_reg
from keyboards.default import user_kb_menu_en, admin_kb_menu, user_kb_menu_ru
from loader import dp

start_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text='🇷🇺 RUS', callback_data='Rus'),
                                        InlineKeyboardButton(text='🇬🇧 ENG', callback_data='Eng')
                                    ]
                                ])

@dp.callback_query_handler(text="Rus")
async def send_message1(call: CallbackQuery):
    await lang_reg(call.from_user.id, 'ru')
    if call.from_user.id in admins:
        await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.bot.send_message(
            chat_id=call.from_user.id,
            text="💼 Админ-мод",
            reply_markup=admin_kb_menu
        )
    else:
        await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.bot.send_message(
            chat_id=call.from_user.id,
            text="💼 Юзер-мод",
            reply_markup=user_kb_menu_ru
        )

@dp.callback_query_handler(text="Eng")
async def send_message(call: CallbackQuery):
    await lang_reg(call.from_user.id, 'en')
    if call.from_user.id in admins:
        await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.bot.send_message(
            chat_id=call.from_user.id,
            text="💼 Админ-мод",
            reply_markup=admin_kb_menu
        )
    else:
        await call.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await call.bot.send_message(
            chat_id=call.from_user.id,
            text="💼 User mode",
            reply_markup=user_kb_menu_en
        )