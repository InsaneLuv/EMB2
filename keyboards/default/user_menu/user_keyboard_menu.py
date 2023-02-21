from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _


user_kb_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📍 Текущие ивенты'),
            KeyboardButton(text='⚒ Инструменты')
        ],
        [
            KeyboardButton(text='👤 Профиль')
        ],
        [
          KeyboardButton(text='🛎 Помощь')
        ]
    ],
    resize_keyboard=True
)

user_kb_menu_en = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📍 Current events'),
            KeyboardButton(text='⚒ Tools')
        ],
        [
            KeyboardButton(text='👤 Profile')
        ],
        [
          KeyboardButton(text='🛎 Help')
        ]
    ],
    resize_keyboard=True
)
