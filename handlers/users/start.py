from aiogram import types

from database import search_profile
from filters import IsSubscriber
from keyboards.inline import start_ikb_menu
from loader import dp, _
from utils.misc import rate_limit


@rate_limit(limit=10)
@dp.message_handler(IsSubscriber(), text='/start')
async def command_start(message: types.Message):
    if message.from_user.username is not None:
        profile = await search_profile("tg_id", message.from_user.id)
        await message.reply(_('Твоё имя - @{username}\n'
                            'Твой id - {id}\n'
                            'Роль - {role}').format(username=message.from_user.username,
                                                    id=message.from_user.id,
                                                    role=profile[2] if profile != None else "None"), reply_markup=start_ikb_menu)
    else:
        await message.reply(_('Твоё имя - 🚫\n'
                            'Твой id - {id}\n\n'
                            '‼ Для дальнейшего пользования ботом настоятельно рекомендую установить юзернейм в настройках профиля, иначе организатору сложнее будет тебя найти.\n'
                            '‼ После, отправь /start ещё раз.').format(id=message.from_user.id))

