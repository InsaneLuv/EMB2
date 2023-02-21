from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='📍 Текущие ивенты'),
            KeyboardButton(text='⚒ Инструменты')
        ],
        [
            KeyboardButton(text='👤 Профиль')
        ],
        [
          KeyboardButton(text='TESTER')
        ]
    ],
    resize_keyboard=True
)
