import traceback

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data.config import admins
from database.events.events import get_rabbit_event_member_count
from loader import dp, _
from tools.destroyed_monuments.dmonuments import get_destroyed_monuments

tools_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        # InlineKeyboardButton(text='🗂 Спарсить газеты', callback_data='Спарсить'),
                                        # InlineKeyboardButton(text='📍 Создать ивент', callback_data='Создать1'),
                                        # InlineKeyboardButton(text='💥 Сломанные монументы', callback_data='dmonuments')
                                        InlineKeyboardButton(text=_('Кол-во участников 🐰🩸'), callback_data='rabbit_event_membercount')
                                    ],
                                    # [
                                    #     InlineKeyboardButton(text='🚨 Troublelogs', callback_data='tlogs'),
                                    #     InlineKeyboardButton(text='🛎 Помощь', callback_data='Помощь')
                                    # ]
                                ])

# rabbit_event_membercount

@dp.callback_query_handler(text="rabbit_event_membercount")
async def rabbit_event_membercount(call: CallbackQuery):
    count = await get_rabbit_event_member_count()
    await call.bot.send_message(chat_id=call.from_user.id, text=_('Текущее количество участников - {count}').format(count=count))

