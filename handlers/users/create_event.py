import simplejson as json
import logging
import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import CallbackQuery

from database.events import event_reg
from filters import AdminCommand
from loader import dp
from states import create_event
from utils.misc import rate_limit
import datetime as dt
from data.config import settings

    # await call.bot.send_message(chat_id=call.from_user.id, text=
    #                             'Ввод информации производится по правилу "1 пункт = 1 строка"\n\n'
    #                             '1.Название ивента\n'
    #                             '2.Описание ивента\n'
    #                             '3.Ссылка на сообщение\n'
    #                             '4.Дата начала(ГГГГ-ММ-ДД)\n'
    #                             '5.Кол-во недель\n'
    #                             '6.Постройки для каждой недели(через запятую)\n')


async def generate_weeks(date,weeks_count) -> list:
    weeks = []
    date = dt.datetime.strptime(date, '%Y-%m-%d')
    d = 0
    for i in range(weeks_count):
        week = dt.date(date.year, date.month, date.day) + dt.timedelta(days=d)
        weeks.append(week.isoformat())
        d += 7
    return weeks


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
        event = answer.split("\n")
        if len(event) != len(settings):
            await message.reply('Not all/More than settings are set\nRegistation canceled')
            await state.finish()
            CancelHandler()
        raw_dict = dict(zip(settings, event))
        data = await state.get_data()
        data['rules'] = [{'count': v, 'type': k} for k,v in raw_dict.items()]
        await state.update_data(data)
    except:
        await message.reply('Ucough, something in input is wrong\nRegistation canceled')
        await state.finish()
        CancelHandler()

    # logging.info(json.dumps(data,indent=4, sort_keys=True, separators=(',', ': '), use_decimal=True))


# @dp.message_handler(state=create_event.title)
# async def state1(message: types.Message, state: FSMContext):
#     answer = message.text
#     await state.update_data(creator_tg_id=message.from_user.id)
#     await state.update_data(title=answer)
#     await message.reply("📄 Описание ивента")
#     await create_event.description.set()


# @dp.message_handler(state=create_event.description)
# async def state2(message: types.Message, state: FSMContext):
#     answer = message.text
#     await state.update_data(description=answer)
#     await message.reply("🔗 Ссылка на сообщение")

#     await create_event.message_url.set()


# @dp.message_handler(state=create_event.message_url)
# async def state3(message: types.Message, state: FSMContext):
#     answer = message.text
#     await state.update_data(message_url=answer)
#     await message.reply("📅 Дата начала ивента в формате\n"
#                         "ГГГГ-ММ-ДД\n"
#                         "Пример: 2023-04-23")
#     await create_event.start_date.set()


# @dp.message_handler(state=create_event.message_url)
# async def state3(message: types.Message, state: FSMContext):
#     answer = message.text
#     await state.update_data(message_url=answer)
#     await message.reply("📅 Дата начала ивента в формате\n"
#                         "ГГГГ-ММ-ДД\n"
#                         "Пример: 2023-04-23")
#     await create_event.start_date.set()


# @dp.message_handler(state=create_event.start_date)
# async def state4(message: types.Message, state: FSMContext):
#     answer = message.text
#     correct_date = await check_date(answer)
#     if correct_date == False:
#             await message.reply("Дата хуйня долбаеб")
#             await state.finish()
#     else:
#         await state.update_data(start_date=answer)
#         await message.reply("🏰 Спец постройки для каждой недели\n(Через запятую)\n"
#                             "Пример: 🌵,🌻,🌹,🌺\n"
#                             )
#         await create_event.buildings.set()


# @dp.message_handler(state=create_event.buildings)
# async def state5(message: types.Message, state: FSMContext):
#     answer = message.text
#     correct_buldings = await check_buildings(answer)
#     if correct_buldings == False:
#         await message.reply("хуйня")
#         await state.finish()
#     else:
#         await state.update_data(buildings=answer.split(","))
#         settings_show = "\n".join(settings)
#         await message.reply('🧬 Points-правила.\n'
#                  'За каждый пункт участник получает определенное вами количество points,\n'
#                  'Например: 5000 убитых крыс - 1 звезда\n\n'
#                  'Вводить значения нужно по очереди за каждый из нижеперечисленных пунктов:\n'
#                  f'{settings_show}\n'
#                  'Каждый пункт - новая строка, пример:\n'
#                  '5000\n'
#                  '2500\nи т.д.\n'
#                  'Таким образом вы выставите значения для s_police и s_police_heli и т.д.\n'
#                  '5000 убитых полицейских = 1 звезда\n'
#                  '2500 убитых вертолётов = 1 звезда. и т.д.')
#         await create_event.settings.set()


# @dp.message_handler(state=create_event.settings)
# async def state6(message: types.Message, state: FSMContext):
#     answer = message.text
#     correct_settings = await check_settings(answer)
#     if correct_settings == False:
#         await message.reply("хуйня")
#         await state.finish()
#     else:
#         await state.update_data(settings=answer.split("\n"))
#         await state.update_data(state="True")
#         await state.update_data(access="*")
#         data = await state.get_data()
#         logging.info(data)




# async def check_date(date) -> str:
#     try:
#         if dt.datetime.strptime(date, '%Y-%m-%d') > dt.datetime.now():
#              return True
#         return False
#     except:
#         return False
    

# async def check_buildings(buildings) -> str:
#     try:
#         if len(buildings.split(",")) == 4:
#             return True
#         return False
#     except:
#         return False


# async def check_settings(input_settings) -> str:
#     try:
#         if len(input_settings.split("\n")) == len(settings):
#             return True
#         return False
#     except:
#         return False    

# async def generate_weeks(date) -> str:


# @dp.message_handler(state=create_event.message_url)
# async def state7(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     title = data.get("title")
#     description = data.get("description")
#     message_url = data.get("message_url")
#     creator = data.get("creator_tg_id")

#     await message.reply("✅ Ивент создан\n\n"
#                         f"🎖 Название: {title}\n"
#                         f"📄 Описание: {description}\n"
#                         f'🔗 Ссылка: {message_url}\n'
#                         f'📣 Организатор:  <a href="tg://user?id={creator}">Ссылка</a>', parse_mode='HTML')
#     await event_reg(state)
    # await state.finish()
