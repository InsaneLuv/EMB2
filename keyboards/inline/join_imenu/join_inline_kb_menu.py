from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from loader import dp

join_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text='Отправить газеты', callback_data='Отправить_газеты')
                                    ],
                                    [
                                        InlineKeyboardButton(text='Сломанные монументы', callback_data='Сломанные_монументы')
                                    ],
                                    [
                                        InlineKeyboardButton(text='🏃🏻 Назад', callback_data='Назад')
                                    ]
                                ])

@dp.callback_query_handler(text="Отправить_газеты")
async def send_message(call: CallbackQuery):
    pass



