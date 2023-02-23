from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database import search_profile
from database.events import event_read, inline_helper, event_update, search_event, get_psettings
from filters import IsSubscriber
from keyboards.inline import edit_ikb_menu
from loader import dp, _
from states import ev_helper, parse_paper_clan
from tools.random_emoji.random_emoji import emoji
from utils.misc import rate_limit


@rate_limit(limit=2)
@dp.message_handler(IsSubscriber(), lambda message: "📍" in message.text)

async def button_current_events_react(message: types.Message):
    event_list = await event_read("current")
    if event_list is not None:
        await dp.bot.send_message(message.from_user.id, _('📍 Выбери интересующий ивент из списка.\n\n'
                                                        '<em>Все ивенты в этом списке проводятся исключительно их организаторами, разработчик бота не отвечает за их проведение и выдачу наград.</em>'),
                                  parse_mode="HTML", reply_markup=genmarkup(message.from_user.id, event_list))
    else:
        await dp.bot.send_message(chat_id=message.from_user.id, text=_("{emoji} Сейчас не проходит никаких ивентов, "
                                                                     "возвращайся позже").format(emoji=emoji()))


@dp.message_handler(state=ev_helper.event)
async def command_any_unknown(message: types.Message, state: FSMContext):
    CancelHandler()
    await state.finish()
    await dp.bot.send_message(chat_id=message.from_user.id, text=_('🚨 Действие отклонено\n'
                                                                 '(Недопустимый ввод)'))


@dp.callback_query_handler(lambda call: True)
async def stoptopupcall(callback_query: types.CallbackQuery, state: FSMContext):
    await dp.bot.answer_callback_query(callback_query.id)
    event = await inline_helper(callback_query.data)
    if event is not None:
        await dp.bot.edit_message_text(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id,
            text=
            f"🎖 Название: {event[1]}\n"
            f"📄 Описание: {event[2]}\n"
            f'🔗 Ссылка: {event[3]}\n',
            parse_mode='HTML',
            reply_markup=gen_event_markup(callback_query.from_user.id, event[0])
        )
        await state.update_data(event=event)
        await ev_helper.next()


@dp.callback_query_handler(state=ev_helper.event)
async def call_organizer1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    event = data.get("event")
    if call.data == "Участвовать":
        profile = await search_profile("tg_id", call.from_user.id)
        if profile is None:
            await dp.bot.answer_callback_query(call.id)
            await dp.bot.send_message(chat_id=call.from_user.id,
                                      text=f'{emoji()} Нельзя принимать участие в ивентах без регистрации профиля.')
            CancelHandler()
            await state.finish()
        else:
            if str(event[5]) != "*":
                access = event[5].split(',')
                if str(call.from_user.id) not in access:
                    await dp.bot.send_message(chat_id=call.from_user.id,
                                              text=f'{emoji()} '
                                                   f'<a href="tg://user?id={event[0]}">Организатор</a> отключил свободное участие.',
                                              parse_mode='HTML')
                    await call.answer()
                else:
                    await dp.bot.delete_message(message_id=call.message.message_id, chat_id=call.from_user.id)
                    await dp.bot.send_message(chat_id=call.from_user.id,
                                              text=_('{emoji} '
                                                   'Отправь газеты.\n\n'
                                                   '(1 строка - 1 ссылка на газету)\n'
                                                   'Не оставляйте пробелы в конце ссылок.').format(emoji=emoji()),
                                              parse_mode='HTML')
                    await parse_paper_clan.paper_clan.set()
                    await call.answer()


            else:
                await dp.bot.send_message(chat_id=call.from_user.id,
                                          text=_('{emoji} '
                                               'Свободное участие сейчас в разработке.').format(emoji=emoji()),
                                          parse_mode='HTML')
                await call.answer()
    elif call.data == "Редактировать":
        await dp.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=
            f"🎖 Название: {event[1]}\n"
            f"📄 Описание: {event[2]}\n"
            f'🔗 Ссылка: {event[3]}\n'
            f'🔑 Доступ: {event[5]}',
            parse_mode='HTML',
            reply_markup=edit_ikb_menu
        )
        await ev_helper.next()
    else:
        event_list = await event_read("current")
        if event_list is not None:
            await dp.bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text=f'📍 Выбери интересующий ивент из списка.\n\n'
                     f'<em>Все ивенты в этом списке проводятся исключительно их организаторами, разработчик бота не '
                     f'отвечает '
                     f'за их проведение и выдачу наград.</em>',
                parse_mode="HTML",
                reply_markup=genmarkup(call.from_user.id, event_list)
            )
            CancelHandler()
            await state.finish()
        else:
            await dp.bot.send_message(chat_id=call.from_user.id,
                                      text=f"{emoji()} Сейчас не проходит никаких ивентов, "
                                           "возвращайся позже")
            CancelHandler()
            await state.finish()


@dp.callback_query_handler(state=ev_helper.editor)
async def event_creator(call: CallbackQuery, state: FSMContext):

    if call.data == "Изменить_название":
        await call.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='🎖 Как назовём ивент?'
        )
        await ev_helper.edit_title.set()

    elif call.data == "Изменить_описание":
        await call.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='📄 Описание ивента'
        )
        await ev_helper.edit_desc.set()

    elif call.data == "Изменить_ссылку":
        await call.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='🔗 Ссылка на сообщение'
        )
        await ev_helper.edit_url.set()

    elif call.data == "Завершить_ивент":
        data = await state.get_data()
        event = data.get("event")
        await event_update("state", "False", event[1])
        event_list = await event_read("current")
        if event_list is not None:
            await dp.bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text=f'📍 Выбери интересующий ивент из списка.\n\n'
                     f'<em>Все ивенты в этом списке проводятся исключительно их организаторами, разработчик бота не '
                     f'отвечает '
                     f'за их проведение и выдачу наград.</em>',
                parse_mode="HTML",
                reply_markup=genmarkup(call.from_user.id, event_list)
            )
            CancelHandler()
            await state.finish()

    elif call.data == "Выдать_доступ":
        await call.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='🔑 Кому выдаём доступ?\n\n'
                 '<em>Введи id через запятую.</em>'
        )
        await ev_helper.edit_access.set()

    
    elif call.data == "points_rules":
        await call.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='🧬 Редактирование points-правил.\n'
                 'За каждый пункт участник получает определенное вами количество points,\n'
                 'Например: 5000 убитых крыс - 1 звезда\n\n'
                 'Вводить значения нужно по очереди за каждый из нижеперечисленных пунктов:\n'
                 's_police\n'
                 's_police_heli\n'
                 's_police_car\n'
                 's_ordinary\n'
                 's_dragons\n'
                 's_pdragons\n'
                 's_alien\n'
                 's_rat\nи т.д.\n'
                 'Каждый пункт - новая строка, пример:\n'
                 '5000\n'
                 '2500\nи т.д.\n'
                 'Таким образом вы выставите значения для s_police и s_police_heli\n'
                 '5000 убитых полицейских = 1 звезда\n'
                 '2500 убитых вертолётов = 1 звезда.'
        )
        await ev_helper.edit_psettings.set()


    elif call.data == "Назад":
        data = await state.get_data()
        event = data.get("event")
        await dp.bot.edit_message_reply_markup(message_id=call.message.message_id, chat_id=call.from_user.id,
                                               reply_markup=gen_event_markup(call.from_user.id, event[0]))
        await ev_helper.event.set()

    

@dp.message_handler(state=ev_helper.edit_title)
async def state10(message: types.Message, state: FSMContext):
    data = await state.get_data()
    event = data.get("event")
    await event_update("name", message.text, event[1])
    new_event = await search_event(message.text)
    await state.update_data(event=new_event)
    await dp.bot.delete_message(message_id=message.message_id,chat_id=message.from_user.id)
    if event is not None:
        await dp.bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=message.message_id,
            text=
            f"🎖 Название: {new_event[1]}\n"
            f"📄 Описание: {new_event[2]}\n"
            f'🔗 Ссылка: {new_event[3]}\n'
            f'🔑 Доступ: {new_event[5]}',
            parse_mode='HTML',
            reply_markup=gen_event_markup(message.from_user.id, new_event[0])
        )
        await ev_helper.event.set()

@dp.message_handler(state=ev_helper.edit_desc)
async def state10(message: types.Message, state: FSMContext):
    data = await state.get_data()
    event = data.get("event")
    await event_update("description", message.text, event[1])
    new_event = await search_event(event[1])
    await state.update_data(event=new_event)
    await dp.bot.delete_message(message_id=message.message_id,chat_id=message.from_user.id)
    if event is not None:
        await dp.bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=message.message_id,
            text=
            f"🎖 Название: {new_event[1]}\n"
            f"📄 Описание: {new_event[2]}\n"
            f'🔗 Ссылка: {new_event[3]}\n'
            f'🔑 Доступ: {new_event[5]}',
            parse_mode='HTML',
            reply_markup=gen_event_markup(message.from_user.id, new_event[0])
        )
        await ev_helper.event.set()

@dp.message_handler(state=ev_helper.edit_url)
async def state10(message: types.Message, state: FSMContext):
    data = await state.get_data()
    event = data.get("event")
    await event_update("url", message.text, event[1])
    new_event = await search_event(event[1])
    await state.update_data(event=new_event)
    await dp.bot.delete_message(message_id=message.message_id,chat_id=message.from_user.id)
    if event is not None:
        await dp.bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=message.message_id,
            text=
            f"🎖 Название: {new_event[1]}\n"
            f"📄 Описание: {new_event[2]}\n"
            f'🔗 Ссылка: {new_event[3]}\n'
            f'📣 Организатор:  tg://user?id={new_event[0]}\n'
            f'🔑 Доступ: {new_event[5]}',
            parse_mode='HTML',
            reply_markup=gen_event_markup(message.from_user.id, new_event[0])
        )
        await ev_helper.event.set()

@dp.message_handler(state=ev_helper.edit_access)
async def state10(message: types.Message, state: FSMContext):
    data = await state.get_data()
    event = data.get("event")
    await event_update("access", message.text, event[1])
    new_event = await search_event(event[1])
    await state.update_data(event=new_event)
    await dp.bot.delete_message(message_id=message.message_id,chat_id=message.from_user.id)
    if event is not None:
        await dp.bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=message.message_id,
            text=
            f"🎖 Название: {new_event[1]}\n"
            f"📄 Описание: {new_event[2]}\n"
            f'🔗 Ссылка: {new_event[3]}\n'
            f'🔑 Доступ: {new_event[5]}',
            parse_mode='HTML',
            reply_markup=gen_event_markup(message.from_user.id, new_event[0])
        )
        await ev_helper.event.set()

@dp.message_handler(state=ev_helper.edit_psettings)
async def state10(message: types.Message, state: FSMContext):
    data = await state.get_data()
    event = data.get("event")
    await event_update("psettings", message.text, event[1])
    new_event = await search_event(event[1])
    await state.update_data(event=new_event)
    await dp.bot.delete_message(message_id=message.message_id,chat_id=message.from_user.id)
    if event is not None:
        await dp.bot.edit_message_text(
        chat_id=message.from_user.id,
        message_id=message.message_id,
            text=
            f"🎖 Название: {new_event[1]}\n"
            f"📄 Описание: {new_event[2]}\n"
            f'🔗 Ссылка: {new_event[3]}\n'
            f'🔑 Доступ: {new_event[5]}\n',
            parse_mode='HTML',
            reply_markup=gen_event_markup(message.from_user.id, new_event[0])
        )
        await ev_helper.event.set()


def genmarkup(intended, data):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for i in data:
        markup.add(InlineKeyboardButton(f"{i[1] if str(intended) != i[0] else i[1] + ' ⭐'}", callback_data=i[1]))
    return markup


def gen_event_markup(intended, event):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(_("🎫 Участвовать"), callback_data="Участвовать"))
    if str(intended) == str(event):
        markup.add(InlineKeyboardButton(f"⚙ Редактировать", callback_data="Редактировать"))
    markup.add(InlineKeyboardButton(_("🏃🏻‍ Назад"), callback_data="Отменить"))
    return markup
