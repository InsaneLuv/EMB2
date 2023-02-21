import os
import time
import traceback
from operator import itemgetter
from datetime import date
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler

from data.config import admins
from database.papers.papers import reg_papers
from loader import dp, _
from loader import bot
from states import parse_paper_clan
from tools.parse_tool_clan.paper_parser_clan import paper_parse_clan
from tools.parse_tool_clan.paper_parser_clan import epit_clan
from tools.troublelogger.troubleloger import troublelog
import re

@dp.message_handler(state=parse_paper_clan.paper_clan)
async def clan_join(message: types.Message, state: FSMContext):
    start_time = time.time()
    test = False
    answer = message.text
    if answer == "z":
        answer = 'https://press.cheapshot.co/view.html?id=fdbcb0b8320424857df9b277f2f842d0%2F3f8a22f4fd1eaae653efef03629ea7b5\n' \
                 'https://press.cheapshot.co/view.html?id=00f05d6d3b8eb1755cdefd17c6bf5091/73165c925c15b6482416a7c1cf00ed36\n' \
                 'https://press.cheapshot.co/view.html?id=b85613a73e94521c6beca7ceb1a3f92f%2F7b2c821d1309645534a8cca5f75ea919\n' \
                 'https://press.cheapshot.co/view.html?id=c2e3d744e588292039d0f43478805f29/6ad8a07869a51aa306603dd809e3c584\n' \
                 'https://press.cheapshot.co/view.html?id=95097c805eaf856cf0c087616023ee19/c006494960a6d6ade1a1aff2ea3e01f3\n'
        test = True
    if not answer.startswith(('https://press.cheapshot.co')):
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
            for admin in admins:
                try:
                    if test is True:
                        await bot.send_document(admin,
                                                document=open(filename, 'rb'),
                                                caption=
                                                f'✉ @{message.from_user.username} прислал газеты.\n'
                                                f'Клан - {result[0]["clantag"]}\n\n'
                                                f'🚨 - ТЕСТОВОЕ СООБЩЕНИЕ - 🚨')
                    else:
                        await bot.send_document(admin,
                                                document=open(filename, 'rb'),
                                                caption=
                                                f'✉ @{message.from_user.username} прислал газеты.\n'
                                                f'Клан - {result[0]["clantag"]}\n')
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
