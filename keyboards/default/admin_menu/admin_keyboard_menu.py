from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='๐ ะขะตะบััะธะต ะธะฒะตะฝัั'),
            KeyboardButton(text='โ ะะฝััััะผะตะฝัั')
        ],
        [
            KeyboardButton(text='๐ค ะัะพัะธะปั')
        ],
        [
          KeyboardButton(text='๐ฝ ๐๐๐๐๐ ๐๐๐๐๐')
        #   KeyboardButton(text='๐ฅฉ ะขะตะบััะธะต ะธะฒะตะฝัั2')
        ]
    ],
    resize_keyboard=True
)
