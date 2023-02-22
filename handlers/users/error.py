import logging
from aiogram import types

from loader import dp, _


@dp.message_handler()
async def command_any_unknown(message: types.Message):
    logging.info(f'[@{message.from_user.username}] entered an unknown command [{message.text}].')
    await message.reply(
        _('🤷🏻 Команды "{message}" не существует.').format(message=message.text)
    )
