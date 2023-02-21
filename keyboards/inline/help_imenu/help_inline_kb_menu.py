from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data.config import technical_messages
from data.config import urls
from loader import dp

help_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text='🧰 Команды', callback_data='Команды'),
                                        InlineKeyboardButton(text='🔩 Зачем этот бот?', callback_data='Зачем1')
                                    ],
                                    [
                                        InlineKeyboardButton(text='🧸 Написать создателю', url=urls['creator'])
                                    ]
                                ])


@dp.callback_query_handler(text="Команды")
async def send_message(call: CallbackQuery):
    await call.bot.edit_message_text(
        text=f'{technical_messages["commands"]}',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=help_ikb_menu
    )


@dp.callback_query_handler(text="Зачем1")
async def send_message(call: CallbackQuery):
    await call.bot.edit_message_text(
        text=f'{technical_messages["For_what"]}',
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=help_ikb_menu
    )