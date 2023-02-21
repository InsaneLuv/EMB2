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
          KeyboardButton(text='👽 𝐀𝐃𝐌𝐈𝐍 𝐓𝐎𝐎𝐋𝐒')
        ]
    ],
    resize_keyboard=True
)
