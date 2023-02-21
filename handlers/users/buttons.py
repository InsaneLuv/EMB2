import random

from aiogram import types

from filters import IsSubscriber
from loader import dp, _
from tools.random_emoji.random_emoji import emoji
from utils.misc import rate_limit


@rate_limit(limit=2)
@dp.message_handler(IsSubscriber(),lambda message: "правила" in message.text.lower())
async def button_rules_react(message: types.Message):
    await message.reply(
        _("{emoji} Эта команда пока в разработке, возвращайся позже").format(emoji=emoji())
    )
