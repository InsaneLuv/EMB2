import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import requests

from data.config import admins
from database import search_profile, search_lang
from filters.admincommand import AdminCommand

from handlers.users.parse_papers_clan import clan_join
from loader import dp, _
from states.test import create_event
from tools.parse_tool_clan.paper_parser_clan import paper_parse_clan
import re

from utils.misc.throttling import rate_limit


tester_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    # [
                                    #     InlineKeyboardButton(text='5 random papers', callback_data='5rp')
                                    # ],
                                    # [
                                    #     InlineKeyboardButton(text='10 papers 🧢', callback_data='10rp1'),
                                    #     InlineKeyboardButton(text='10 papers [B4]', callback_data='10rp2')
                                    # ],
                                    # [
                                    #     InlineKeyboardButton(text='🚽 CLEAN ALL', callback_data='clean')
                                    # ],
                                    # [
                                    #     InlineKeyboardButton(text='localization checker', callback_data='localization')
                                    # ],
                                    [
                                        InlineKeyboardButton(text='create event', callback_data='create_event')
                                    ]
                                ])


eventtype_ikb_menu = InlineKeyboardMarkup(row_width=2,
                                inline_keyboard =[
                                    [
                                        InlineKeyboardButton(text='Clan Event', callback_data='clan_event'),
                                        InlineKeyboardButton(text='Squi hate', callback_data='hater'),
                                        InlineKeyboardButton(text='🐰🩸 Event', callback_data='rabbit_event')
                                    ]
                                ])


@rate_limit(limit=3600)
@dp.callback_query_handler(AdminCommand(),text="create_event")
async def event_creator(call: CallbackQuery):
    await call.bot.send_message(chat_id=call.from_user.id, text=f'Выбери тип ивента\n(отображены только доступные).',reply_markup=eventtype_ikb_menu)
    await create_event.type.set()
