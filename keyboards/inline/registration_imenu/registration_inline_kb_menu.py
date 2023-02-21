from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

registration_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text='✅ Пройти регистрацию', callback_data='Пройти'),
                                        InlineKeyboardButton(text='⛔ Отменить действие', callback_data='Отменить')
                                    ]
                                ])

yes_no_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text='✅ Да, это я', callback_data='Да'),
                                        InlineKeyboardButton(text='⛔ Отменить действие', callback_data='Отменить2')
                                    ]
                                ])
