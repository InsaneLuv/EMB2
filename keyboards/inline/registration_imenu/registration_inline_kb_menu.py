from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import _

registration_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text=_('✅ Пройти регистрацию'), callback_data='Пройти'),
                                        InlineKeyboardButton(text=_('⛔ Отменить действие'), callback_data='Отменить')
                                    ]
                                ])

yes_no_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text=_('✅ Да, это я'), callback_data='Да'),
                                        InlineKeyboardButton(text=_('⛔ Отменить действие'), callback_data='Отменить2')
                                    ]
                                ])
