from collections import Counter
import os
import time
import traceback
from operator import itemgetter
from datetime import date
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler

from data.config import admins, test_paper
from database.papers.papers import reg_papers
from database.profile.profile import search_profile
from loader import dp, _
from loader import bot
from states import parse_paper_clan
from tools.parse_tool_clan.paper_parser_clan import paper_parse_clan
from tools.parse_tool_clan.paper_parser_clan import epit_clan
from tools.troublelogger.troubleloger import troublelog
import re


async def answer_handler(message):
    answer = message.text

    try:
        answer = int(answer)
        answer = test_paper[answer]
    except:
        answer = message.text

    if not answer.startswith(('https://press.cheapshot.co')):
        return False
    else:
        return answer

    


@dp.message_handler(state=parse_paper_clan.paper_clan)
async def clan_join(message: types.Message, state: FSMContext):
    start_time = time.time()
    answer = await answer_handler(message)
    if answer is False:
        await bot.send_message(chat_id=message.from_user.id, text=_('🚨 Действие отменено\n'
                                                                '(Некорректная ссылка)'))
        CancelHandler()
        await state.finish()
    else:
        try:
            await message.answer_chat_action("upload_document")

            a = await bot.send_message(chat_id=message.from_user.id, text=_('- Компановка газет...'))
            paper = answer
            paper = re.sub('\n\n\n', '\n', paper)
            paper = re.sub('\n\n', '\n', paper)
            paper = re.sub('\n', ',', paper)
            paper_re = re.sub('%2F', '/', paper)
            paper_re = re.sub('%20', '', paper_re)
            answer = re.sub(' ', '', paper_re)

            if answer[len(answer) - 1] == ',':
                answer = answer[:len(answer) - 1]

            a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=a.message_id, text=_('{a}\n- Запись запроса в бд...').format(a=a.text))

            await reg_papers(message.from_user.id, str(answer), str(date.today()))

            a = await bot.edit_message_text(chat_id=message.from_user.id,message_id=a.message_id,text=_('{a}\n- Парсинг газет...').format(a=a.text))
            result = await paper_parse_clan(answer, "event")

            a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=a.message_id,text=_('{a}\n- Сортировка...').format(a=a.text))

            try:
                result.sort(key=itemgetter('username'))
            except:
                pass
            a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=a.message_id, text=_('{a}\n- Загрузка данных в таблицу...').format(a=a.text))
            filename = await epit_clan(result, message.from_user.id,'🌲')
            a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=a.message_id, text=_('{a}\n- Отправка таблицы организатору...').format(a=a.text))
            from_profile = await search_profile('tg_id',message.from_user.id)
            list_of_clans = []
            for i in result:
                list_of_clans.append(i['clanname'])

            list_of_clans = Counter(list_of_clans)
            
            if message.from_user.id in admins:
                test = True
            else:
                test = False

                
            for admin in admins:
                try:
                    if test is True:
                        await bot.send_document(admin,
                        document=open(filename, 'rb'),
                        caption=
                        f'📥: <a href="https://t.me/{message.from_user.username}">{from_profile[1]}</a>\n'
                        f'👨‍👨‍👦‍👦: {",".join(str(f"{clan}({count})") for clan,count in list_of_clans.items())} \n'
                        f'📆: {result[0]["date"]}\n'
                        f'🚨 - ТЕСТОВОЕ СООБЩЕНИЕ - 🚨', parse_mode="HTML")
                    else:
                        await bot.send_document(admin,
                        document=open(filename, 'rb'),
                        caption=
                        f'📥: <a href="https://t.me/{message.from_user.username}">{from_profile[1]}</a>\n'
                        f'👨‍👨‍👦‍👦: {",".join(str(f"{clan}({count})") for clan,count in list_of_clans.items())} \n'
                        f'📆: {result[0]["date"]}', parse_mode="HTML")
                except:
                    pass
            a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=a.message_id,
                                        text=_('{a}\n- Удаление остаточных файлов...').format(a=a.text))
            if os.path.exists(filename):
                os.remove(filename)
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=a.message_id,
                                        text=_('{a}\n\n✅ Газеты отправлены организатору, спасибо за участие!').format(a=a.text))
            CancelHandler()
            await state.finish()
        except Exception:
            e = traceback.format_exc()
            await troublelog(message.from_user.username, e, answer)
            await bot.send_message(chat_id=message.from_user.id, text=f'🚨 ОШИБКА\n'
                                                                      f'{e}\n\n'
                                                                      f'Информация об ошибке уже отправлена разработчику бота, если есть вопросы - пишите:\n'
                                                                      f'@spaghetti_coder')

            for admin in admins:
                await bot.send_message(chat_id=admin,
                                       text=f'🚨 @{message.from_user.username} получил ошибку, ошибка внесена в troublelogs.\n {e}')
            CancelHandler()
            await state.finish()
