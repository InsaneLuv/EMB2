from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

event_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text='Учавствовать', callback_data='Учавствовать')
                                    ],
                                    [
                                        InlineKeyboardButton(text='Редактировать', callback_data='Редактировать')
                                    ],
                                    [
                                        InlineKeyboardButton(text='Отменить', callback_data='Отменить2')
                                    ],
                                ])

edit_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text='🎖 Название', callback_data='Изменить_название'),
                                        InlineKeyboardButton(text='📄 Описание', callback_data='Изменить_описание'),
                                        InlineKeyboardButton(text='🔗 Ссылка', callback_data='Изменить_ссылку')
                                    ],
                                    [
                                        InlineKeyboardButton(text='🔑 Выдать доступ',callback_data='Выдать_доступ')
                                    ],
                                    [
                                        InlineKeyboardButton(text='🧬 Points-правила', callback_data='points_rules')
                                    ],
                                    [
                                        InlineKeyboardButton(text='⛔ Завершить ивент', callback_data='Завершить_ивент')
                                    ],
                                    [
                                        InlineKeyboardButton(text='🏃🏻 Назад', callback_data='Назад')
                                    ]
                                ])

edit_ikb_menu_back = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text='🏃🏻 Назад', callback_data='Назад')
                                    ]
                                ])

cancel_edit_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text='Отменить', callback_data='Отменить_действие')
                                    ]
                                ])
