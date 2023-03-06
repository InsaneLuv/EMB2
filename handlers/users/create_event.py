import uuid
import simplejson as json
import logging
import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import CallbackQuery

from database.events import event_reg
from database.events.events import event_reg2
from filters import AdminCommand
from loader import dp, bot
from states import create_event
from utils.misc import rate_limit
import datetime as dt
from data.config import settings

async def generate_weeks(date,weeks_count) -> list:
    weeks = []
    date = dt.datetime.strptime(date, '%Y-%m-%d')
    d = 0
    for i in range(weeks_count):
        week = dt.date(date.year, date.month, date.day) + dt.timedelta(days=d)
        weeks.append(week.isoformat())
        d += 7
    return weeks

@dp.callback_query_handler(state=create_event.type)
async def event_type_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if call.data == 'hater':
        await call.bot.send_message(chat_id=call.from_user.id, text=
                    'Ввод информации производится по правилу "1 пункт = 1 строка"\n\n'
                    '1.Название ивента\n'
                    '2.Описание ивента\n'
                    '3.Ссылка на сообщение\n'
                    '\n\n'
                    '*Дата начала = дата принятия первых газет, всегда воскресенье.')
        data['type'] = call.data
        await state.update_data(data)
        await create_event.maker_other.set()
    elif call.data == 'clan_event':
        await call.bot.send_message(chat_id=call.from_user.id, text=
                            'Ввод информации производится по правилу "1 пункт = 1 строка"\n\n'
                            '1.Название ивента\n'
                            '2.Описание ивента\n'
                            '3.Ссылка на сообщение\n'
                            '4.Дата начала(ГГГГ-ММ-ДД)\n'
                            '5.Кол-во недель\n'
                            '6.Постройки для каждой недели(через запятую)\n')
        data['type'] = call.data
        await state.update_data(data)
        await create_event.maker.set()
    elif call.data == 'rabbit_event':
        await call.bot.send_message(chat_id=call.from_user.id, text=
                    'Ввод информации производится по правилу "1 пункт = 1 строка"\n\n'
                    '1.Название ивента\n'
                    '2.Описание ивента\n'
                    '3.Ссылка на сообщение\n'
                    '\n\n'
                    '*Дата начала = дата принятия первых газет, всегда воскресенье.')
        data['type'] = call.data
        await state.update_data(data)
        await create_event.maker_other.set()
    else:
        await state.finish()
        CancelHandler()

@dp.message_handler(state=create_event.maker)
async def maker(message: types.Message, state: FSMContext):
    try:
        points = [
            'title',
            'description',
            'message_link',
            'date_start',
            'weeks_count',
            'special'
        ]
        answer = message.text
        if answer == 'z':
            answer = 'CLAN WARS\nDescr\nurl_to_message\n2023-02-26\n4\n🌵,🌻,🌹,🌺'
        event = answer.split("\n")
        raw_dict = dict(zip(points, event))
        raw_dict['weeks_count'] = int(raw_dict.pop('weeks_count', len(raw_dict['special'].split(","))))

        if len(raw_dict['special'].split(",")) != raw_dict['weeks_count']:
            await message.reply('Buildings count must be equal to weeks count\nRegistation canceled')
            await state.finish()
            CancelHandler()

        if dt.datetime.strptime(raw_dict['date_start'], '%Y-%m-%d').weekday() != 6:
            await message.reply('Start date must be on Sunday\nRegistation canceled')
            await state.finish()
            CancelHandler()

        datelist = await generate_weeks(raw_dict['date_start'], raw_dict['weeks_count'])

        raw_dict['weeks'] = []

        for i in range(len(datelist)):
            raw_dict['weeks'].append({'special_building': raw_dict['special'].split(",")[i], 'date':datelist[i]})

        raw_dict.pop("weeks_count", None)
        raw_dict.pop("date_start", None)
        raw_dict.pop("special", None)
        
        await state.update_data(raw_dict)

        settings_show = "\n".join(settings)
        await message.reply('🧬 Points-правила.\n'
                'За каждый пункт участник получает определенное вами количество points,\n'
                'Например: 5000 убитых крыс - 1 звезда\n\n'
                'Вводить значения нужно по очереди за каждый из нижеперечисленных пунктов:\n'
                f'{settings_show}\n'
                'Каждый пункт - новая строка, пример:\n'
                '5000\n'
                '2500\nи т.д.\n'
                'Таким образом вы выставите значения для s_police и s_police_heli и т.д.\n'
                '5000 убитых полицейских = 1 звезда\n'
                '2500 убитых вертолётов = 1 звезда. и т.д.')
        await create_event.s_setler.set()
    except:
        await message.reply('Ucough, something in input is wrong\nRegistation canceled')
        await state.finish()
        CancelHandler()


@dp.message_handler(state=create_event.s_setler)
async def s_setler(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if answer == 'z':
            answer = '5000\n2500\n250\n1000\n50\n25\n25\n5000\n2'
        event = answer.split("\n")
        if len(event) != len(settings):
            await message.reply('Not all/More than settings are set\nRegistation canceled')
            await state.finish()
            CancelHandler()
        raw_dict = dict(zip(settings, event))
        data = await state.get_data()
        data['rules'] = [{'count': v, 'type': k} for k,v in raw_dict.items()]
        data['creator_id'] = message.from_user.id
        data['uuid'] = uuid.uuid4()
        await state.update_data(data)
        await event_reg2(state)
        await state.finish()
        CancelHandler()
    except:
        await message.reply('Ucough, something in input is wrong\nRegistation canceled')
        await state.finish()
        CancelHandler()


@dp.message_handler(state=create_event.maker_other)
async def maker2(message: types.Message, state: FSMContext):
    points = [
        'title',
        'description',
        'message_link'
    ]
    answer = message.text
    event = answer.split("\n")
    raw_dict = dict(zip(points, event))
    raw_dict['creator_id'] = message.from_user.id
    raw_dict['uuid'] = uuid.uuid4()
    await state.update_data(raw_dict)
    await event_reg2(state)
    await state.finish()
    CancelHandler()
