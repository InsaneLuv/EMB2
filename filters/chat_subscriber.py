from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from data.config import chat_ids
from loader import bot, dp

markup = InlineKeyboardMarkup(row_width=2,
                              inline_keyboard=[
                                  [
                                      InlineKeyboardButton(text='❤ Подписаться',
                                                           url='https://t.me/cheapshot_event_manager')
                                  ],
                                  [
                                      InlineKeyboardButton(text='🤔 Зачем?', callback_data='Зачем')
                                  ]
                              ])

class IsSubscriber(BoundFilter):
    async def check(self, message: types.Message):
        for chat_id in chat_ids:
            sub = await bot.get_chat_member(chat_id=chat_id,user_id=message.from_user.id)
            if sub.status != types.ChatMemberStatus.LEFT:
                return True
            else:
                await dp.bot.delete_message(message.chat.id, message.message_id)
                await dp.bot.send_message(chat_id=message.from_user.id,
                                          text=f'🚨 Для пользования ботом обязательна подписка на наш телеграм-канал.\n\n'
                                               f'Подпишись и отправь  команду "{message.text}" ещё раз.',reply_markup=markup)
                raise CancelHandler()

    @dp.callback_query_handler(text="Зачем")
    async def send_message(call: CallbackQuery):
        try:
            await call.bot.edit_message_text(
                text='🚨 Для пользования ботом обязательна подписка на наш телеграм-канал.\n\n'
                     '❤ Ваша подписка - это благодарность за труды и мотивация для дальнейшей разработки.\n\n'
                     '🧡 В канале вы можете узнать новости о проводимых ивентах, их итогах и прочем.',
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                reply_markup=markup
            )
        except Exception as e:
            print(e)