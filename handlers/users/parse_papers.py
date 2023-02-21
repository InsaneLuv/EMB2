import os
import time
from time import gmtime, strftime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import CallbackQuery

from keyboards.inline import file_or_message_ikb_menu
from loader import dp, bot
from states import parse_paper
from tools.parse_tool.paper_parser import paper_parse, epit


@dp.callback_query_handler(text="Спарсить")
async def event_creator(call: CallbackQuery):
    await call.bot.send_message(chat_id=call.from_user.id, text='🗂 Введи газеты, где каждая газета - новая строка.')
    await parse_paper.paper.set()


@dp.message_handler(state=parse_paper.paper)
async def state1(message: types.Message, state: FSMContext):
    start_time = time.time()
    answer = message.text
    print(answer)
    if answer == "z":
        answer = "https://press.cheapshot.co/view.html?id=1a171089cafe29bb38e87281d14862d2%2F344f98de4351793f391379539b625051\n" \
                 "https://press.cheapshot.co/view.html?id=ddb27ad5713275159e522e8a3d909252%2F98ce05f52e8fca5f9ff2e3747d76dc84\n" \
                 "https://press.cheapshot.co/view.html?id=ddb27ad5713275159e522e8a3d909252%2F207f307152e3506ca5e8106463a221f8"
    if not answer.startswith(('https://press.cheapshot.co', 'http://press.cheapshot.co', 'press.cheapshot.co')):
        await bot.send_message(chat_id=message.from_user.id, text='🚨 Действие отменено\n'
                                                                  '(Некорректная ссылка)')
        CancelHandler()
        await state.finish()
    else:
        await state.update_data(paper=answer)
        data = await state.get_data()
        papers = data.get("paper")
        result = await paper_parse(papers)
        await state.update_data(raw_result=result)
        count = 0
        outmessages = []
        for owner, items in result.items():
            count += 1
            outmessage = f"Газета №{count}.\n\n" \
                         f"{items['date'] if 'date' in items else '00.00.00'}\n" \
                         f"{items['userpic'] if 'userpic' in items else '???'} {items['username'] if 'username' in items else '???'}\n\n" \
                         f"👮‍: {items['police'] if 'police' in items else '0'}\n" \
                         f"🚁‍: {items['police_heli'] if 'police_heli' in items else '0'}\n" \
                         f"🐝‍: {items['birdie'] if 'birdie' in items else '0'}\n" \
                         f"🦀‍: {items['ordinary'] if 'ordinary' in items else '0'}\n" \
                         f"🐉‍: {items['dragon'] if 'dragon' in items else '0'}\n" \
                         f"👾‍: {items['alien'] if 'alien' in items else '0'}\n" \
                         f"🚔‍: {items['police_car'] if 'police_car' in items else '0'}\n" \
                         f"🐀‍: {items['rat'] if 'rat' in items else '0'}\n\n"
            outmessages.append(outmessage)
            await state.update_data(paper_result=outmessages)

        await message.bot.send_message(chat_id=message.from_user.id,
                                       text=f'🗂 Готово, спарсил {count} газет за {time.time() - start_time: 0.2f} секунд.\n'
                                            f'В каком виде отправить результат?', reply_markup=file_or_message_ikb_menu)
        await parse_paper.next()


@dp.callback_query_handler(state=parse_paper.save)
async def call1(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    papers_result = data.get("paper_result")
    if call.data == "Файл":
        timestamp = strftime("%H-%M-%S", gmtime())
        filename = f'res_{call.from_user.id}_{str(timestamp)}.txt'
        for i in papers_result:
            with open(filename, 'ab') as writer:
                writer.write(i.encode("utf-8"))
        await bot.send_document(call.from_user.id, open(filename, 'rb'))
        if os.path.exists(filename):
            os.remove(filename)
    elif call.data == "Сообщение":
        for i in papers_result:
            await bot.send_message(chat_id=call.from_user.id, text=i)
    elif call.data == "Таблица":
        raw_result = data.get("raw_result")
        filename = await epit(raw_result, call.from_user.id)
        await bot.send_document(call.from_user.id, open(filename, 'rb'))
        if os.path.exists(filename):
            os.remove(filename)
    CancelHandler()
    await state.finish()
