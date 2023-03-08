from aiogram import types

from database import search_profile
from database.profile.profile import lang_reg
from filters import IsSubscriber
from keyboards.inline import start_ikb_menu
from loader import dp, _
from utils.misc import rate_limit


@rate_limit(limit=10)
@dp.message_handler(IsSubscriber(), text='/start')
async def command_start(message: types.Message):
    await lang_reg(message.from_user.id, 'ru')
    if message.from_user.username is not None:
        profile = await search_profile("tg_id", message.from_user.id)
        await message.reply(_('Выберите язык.\nChoose language.'), reply_markup=start_ikb_menu)
    else:
        await message.reply(_('Для пользования ботом вам нужно установить юзернейм в профиле телеграм.\nЭто нужно для того, что бы организатор мог связаться с вами для выдачи награды.\n<a href="https://web-telegramm.org/telegramm/web/608-kak-zapolnit-username-v-telegramme.html">Инструкция.</a>'),parse_mode="HTML")

