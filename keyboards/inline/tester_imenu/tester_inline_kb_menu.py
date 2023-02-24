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
                                    [
                                        InlineKeyboardButton(text='5 random papers', callback_data='5rp')
                                    ],
                                    [
                                        InlineKeyboardButton(text='10 papers 🧢', callback_data='10rp1'),
                                        InlineKeyboardButton(text='10 papers [B4]', callback_data='10rp2')
                                    ],
                                    [
                                        InlineKeyboardButton(text='🚽 CLEAN ALL', callback_data='clean')
                                    ],
                                    [
                                        InlineKeyboardButton(text='localization checker', callback_data='localization')
                                    ],
                                    [
                                        InlineKeyboardButton(text='create event', callback_data='create_event')
                                    ]
                                ])

@dp.callback_query_handler(text="5rp")
async def call5rp(call: CallbackQuery):
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    a = await call.bot.send_message(chat_id=call.from_user.id, text=f'- Process')
    answer = 'https://press.cheapshot.co/view.html?id=fdbcb0b8320424857df9b277f2f842d0%2F3f8a22f4fd1eaae653efef03629ea7b5\n' \
             'https://press.cheapshot.co/view.html?id=00f05d6d3b8eb1755cdefd17c6bf5091/73165c925c15b6482416a7c1cf00ed36\n' \
             'https://press.cheapshot.co/view.html?id=b85613a73e94521c6beca7ceb1a3f92f%2F7b2c821d1309645534a8cca5f75ea919\n' \
             'https://press.cheapshot.co/view.html?id=c2e3d744e588292039d0f43478805f29/6ad8a07869a51aa306603dd809e3c584\n' \
             'https://press.cheapshot.co/view.html?id=95097c805eaf856cf0c087616023ee19/c006494960a6d6ade1a1aff2ea3e01f3\n'
    paper = answer
    paper = re.sub('\n\n\n', '\n', paper)
    paper = re.sub('\n\n', '\n', paper)
    paper = re.sub('\n', ',', paper)
    paper_re = re.sub('%2F', '/', paper)
    paper_re = re.sub('%20', '', paper_re)
    answer = re.sub(' ', '', paper_re)

    if answer[len(answer) - 1] == ',':
        answer = answer[:len(answer) - 1]
    result = await paper_parse_clan(answer, "event")
    await call.bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=a.message_id,
        text=f"{len(result)} papers done, whats next?",
        reply_markup=tester_ikb_menu
    )

@dp.callback_query_handler(text="10rp1")
async def call5rp(call: CallbackQuery):
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    a = await call.bot.send_message(chat_id=call.from_user.id, text=f'- Process')
    answer = 'https://press.cheapshot.co/view.html?id=d06a4ff0411c19d85589793707a95da9/bf26196f46e9391e1e74f52da8b0ffe0,https://press.cheapshot.co/view.html?id=e86c3f4272998cdfbd0964b10ad43a54/241f55cea7adfebc03f260cf61638c3f,https://press.cheapshot.co/view.html?id=064e2298ffd141f02bd5733f4d49ab28/d48ec3b7b3e15df5cdf8f9d10f731083,https://press.cheapshot.co/view.html?id=30539d4e9861e8bffbe557d0c9341e0d/2acd8e3d52065878f10c1e821ca542e8,https://press.cheapshot.co/view.html?id=113d50b61f9a889ed80285bf9608d6e3/064f97aab8265187a3d4ce638665b58f,https://press.cheapshot.co/view.html?id=79bad88c401c5e4a671dc7410938d94b/4685486865332ca6fa511e29b849384e,https://press.cheapshot.co/view.html?id=b437d20e189d89662e4b8f500a1f28aa/0a543a0df614ab00621dd5b834cc3545,https://press.cheapshot.co/view.html?id=2fcf3ed1be93ae7f56af1486c05ba09c/34719f35f6fca8fc3a59bef304e9f775,https://press.cheapshot.co/view.html?id=03273ace499efd3b93130889f9797c8b/4f34547572aec1009b97e6f6a55c83f1,https://press.cheapshot.co/view.html?id=19eb954abf9ba2f953cc73119f651707/f1c32552e1356a8d26b67cdfe0d07de2'
    paper = answer
    paper = re.sub('\n\n\n', '\n', paper)
    paper = re.sub('\n\n', '\n', paper)
    paper = re.sub('\n', ',', paper)
    paper_re = re.sub('%2F', '/', paper)
    paper_re = re.sub('%20', '', paper_re)
    answer = re.sub(' ', '', paper_re)

    if answer[len(answer) - 1] == ',':
        answer = answer[:len(answer) - 1]
    result = await paper_parse_clan(answer, "event")
    await call.bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=a.message_id,
        text=f"{len(result)} papers done, whats next?",
        reply_markup=tester_ikb_menu
    )

@dp.callback_query_handler(text="10rp2")
async def call5rp(call: CallbackQuery):
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    a = await call.bot.send_message(chat_id=call.from_user.id, text=f'- Process')
    answer = 'https://press.cheapshot.co/view.html?id=af6b6a5a31709ce55e059bade76297c6/6c941a01519087347d7d657268b6a7a7,https://press.cheapshot.co/view.html?id=c2e3d744e588292039d0f43478805f29/10a49cb2fd0eb92f3b02b4f73ba93a2b,https://press.cheapshot.co/view.html?id=dabc0395c4c2c1753a05ee5fe0a2c988/f9342c98ef4438d7db1e3ab63e2022ac,https://press.cheapshot.co/view.html?id=74902740c1bd984b649e453ad136b294/a8493b9abe8c8615e217b922e76d1078,https://press.cheapshot.co/view.html?id=bac05229870c71fa6d298015514650f4/9021fd9c11754bd4ff88f463225a3487,https://press.cheapshot.co/view.html?id=2480e9e4a6e2b0fce3d03731e5e2dfe7/dedf8b397d59a3c63defaeedc1bc9113,https://press.cheapshot.co/view.html?id=e33740006caff9487ed0128dec324346/707d9217a34944168f659b38f18157d4,https://press.cheapshot.co/view.html?id=9670156f2c736094fe457db761f1acb1/3a67f7c8ba18e5493c8f174f5ace8184,https://press.cheapshot.co/view.html?id=eeae7052922182e4a3e0d031388e17b6/8176d9cb438656371302ceb51081e50c,https://press.cheapshot.co/view.html?id=a080677bc891c10f2c2ab9e11c10e210/7e6b11c35abf994e23694eb01c040619'
    paper = answer
    paper = re.sub('\n\n\n', '\n', paper)
    paper = re.sub('\n\n', '\n', paper)
    paper = re.sub('\n', ',', paper)
    paper_re = re.sub('%2F', '/', paper)
    paper_re = re.sub('%20', '', paper_re)
    answer = re.sub(' ', '', paper_re)

    if answer[len(answer) - 1] == ',':
        answer = answer[:len(answer) - 1]
    result = await paper_parse_clan(answer, "event")
    await call.bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=a.message_id,
        text=f"{len(result)} papers done, whats next?",
        reply_markup=tester_ikb_menu
    )

@dp.callback_query_handler(text="clean")
async def call5rp(call: CallbackQuery):
    await call.bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    a = await call.bot.send_message(chat_id=call.from_user.id, text=f'- Process')
    api_url = 'http://141.8.199.204:9000/clanevent/newspaper'
    api_clear_url = 'http://141.8.199.204:9000/clanevent/newspaper/clear'
    headers = {'Content-type': 'application/json',
               'Accept': 'text/plain',
               'Content-Encoding': 'utf-8'}

    requests.post(api_clear_url, data={}, headers=headers)

    await call.bot.edit_message_text(
        chat_id=call.from_user.id,
        message_id=a.message_id,
        text=f"clean done, whats next?",
        reply_markup=tester_ikb_menu
    )

@dp.callback_query_handler(text="localization")
async def call5rp(call: CallbackQuery):
    lang = await search_lang(call.from_user.id)
    await call.bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=_('ЛОКАЛИЗАЦИЯ'),reply_markup=tester_ikb_menu)
    await call.answer()

@rate_limit(limit=3600)
@dp.callback_query_handler(AdminCommand(),text="create_event")
async def event_creator(call: CallbackQuery):
    await call.bot.send_message(chat_id=call.from_user.id, text=
                                'Ввод информации производится по правилу "1 пункт = 1 строка"\n\n'
                                '1.Название ивента\n'
                                '2.Описание ивента\n'
                                '3.Ссылка на сообщение\n'
                                '4.Дата начала(ГГГГ-ММ-ДД)\n'
                                '5.Кол-во недель\n'
                                '6.Постройки для каждой недели(через запятую)\n')
    await create_event.maker.set()
