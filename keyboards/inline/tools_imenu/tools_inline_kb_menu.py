import traceback

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data.config import admins
from database.events.events import get_rabbit_event_member_count
from loader import dp
from tools.destroyed_monuments.dmonuments import get_destroyed_monuments

tools_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        # InlineKeyboardButton(text='🗂 Спарсить газеты', callback_data='Спарсить'),
                                        # InlineKeyboardButton(text='📍 Создать ивент', callback_data='Создать1'),
                                        # InlineKeyboardButton(text='💥 Сломанные монументы', callback_data='dmonuments')
                                        InlineKeyboardButton(text='Кол-во участников 🐰🩸', callback_data='rabbit_event_membercount')
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
    await call.bot.send_message(chat_id=call.from_user.id, text=f'Текущее количество участников - {count}')

@dp.callback_query_handler(text="dmonuments")
async def send_message(call: CallbackQuery):
    try:
        dmonuments = await get_destroyed_monuments()
        lst_str = "\n".join(str(e) for e in dmonuments)
        await call.bot.send_message(chat_id=call.from_user.id, text=f'💥 Сломанные монументы:\n'
                                                                    f'{lst_str}')
    except Exception:
        e = traceback.format_exc()
        await call.bot.send_message(chat_id=call.from_user.id, text=f'🚨 ОШИБКА\n'
                                                                  f'{e}\n\n'
                                                                  f'Информация об ошибке уже отправлена разработчику бота, если есть вопросы - пишите:\n'
                                                                  f'@spaghetti_coder')

        for admin in admins:
            await call.bot.send_message(chat_id=admin,
                                   text=f'🚨 @{call.from_user.username} получил ошибку\n {e}')

