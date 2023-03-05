import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, location, ContentTypes
from aiogram.utils.markdown import hlink
from database import search_profile
from database.events import event_read, inline_helper, event_update, search_event, get_psettings
from database.events.events import append_to_access, deny_access_by_tg_id, get_by_uuid, get_eventlist, reg_paper
from filters import IsSubscriber
from keyboards.inline import edit_ikb_menu
from loader import dp, _, bot
from states import ev_helper, parse_paper_clan
from tools.parse_other.parser import SheetsClient
from tools.random_emoji.random_emoji import emoji
from utils.misc import rate_limit
from tools import Parser



@rate_limit(limit=2)
@dp.message_handler(IsSubscriber(), lambda message: "📍" in message.text)
async def button_current_events_react(message: types.Message, state: FSMContext):
    await state.update_data(message_id=message.message_id)
    event_list = await get_eventlist()
    if event_list is not None:
        await bot.send_message(message.from_user.id, _('📍 Выбери интересующий ивент из списка.\n\n'
                                                        '<em>📣 Все ивенты в этом списке проводятся исключительно их организаторами, разработчик бота не отвечает за их проведение и выдачу наград.</em>'),parse_mode="HTML", reply_markup=genmarkup(message.from_user.id, event_list))
    else:
        await bot.send_message(chat_id=message.from_user.id, text=_("{emoji} Сейчас не проходит никаких ивентов, "
                                                                     "возвращайся позже").format(emoji=emoji()))

@dp.message_handler(state=ev_helper.event)
async def command_any_unknown(message: types.Message, state: FSMContext):
    data = await state.get_data()
    msgid = data.get("message_id")
    await bot.delete_message(message_id=msgid, chat_id=message.from_user.id)
    await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
    CancelHandler()
    await state.finish()
    await dp.bot.send_message(chat_id=message.from_user.id, text=_('🚨 Действие отклонено\n(Повторите попытку)'))

@dp.callback_query_handler(lambda call: True)
async def stoptopupcall(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(message_id=callback_query.message.message_id)
    await dp.bot.answer_callback_query(callback_query.id)
    event = await get_by_uuid(callback_query.data)
    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=f"🎖 Название: {event['event_title']}\n"
            f"📄 Описание: {event['event_description']}\n"
            f"🔗 Ссылка: {event['event_message_url']}\n",
        reply_markup=gen_event_markup(callback_query.from_user.id, event)
    )
    await state.update_data(event=event)
    await ev_helper.next()

@dp.callback_query_handler(state=ev_helper.event)
async def call_organizer1(call: CallbackQuery, state: FSMContext):
    await state.update_data(message_id=call.message.message_id)
    data = await state.get_data()
    event = data.get("event")
    access = True
    if call.data == "Участвовать":
        profile = await search_profile("tg_id", call.from_user.id)
        if profile is None:
            await return_popup_error(call.id, 'Нельзя принимать участие в ивенте без регистрации профиля.')
            access = False

        if event["access"] is not None:
            access_list = {i['tg_id']: i for i in event["access"]}
            if call.from_user.id not in access_list:
                await return_popup_error(call.id, 'У вас нет доступа к участию в ивенте.')
                access = False

        if access:
            if event['type'] != 'clan_event':
                await dp.bot.edit_message_text(
                chat_id=call.from_user.id,
                message_id=call.message.message_id,
                text=f'🗞 Отправь газету.'
                )
                await ev_helper.parser.set()
            else:
                await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
                CancelHandler()
                await state.finish()
        else:
            await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
            CancelHandler()
            await state.finish()
            
    elif call.data == "Редактировать":
        await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"🎖 Название: {event['event_title']}\n"
            f"📄 Описание: {event['event_description']}\n"
            f"🔗 Ссылка: {event['event_message_url']}\n"
            f"📖 Тип ивента: {event['type']}",
        reply_markup=gen_edit_markup(event)
        )
        await ev_helper.next()
    else:
        event_list = await get_eventlist()
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
    data = await state.get_data()
    event = data.get("event")
    if call.data == "Выдать_доступ":
        await call.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='🔑 Кому выдаём доступ?\n\n'
                 '<em>Введи id через запятую.</em>'
        )
        await ev_helper.edit_access.set()
    elif call.data == "Забрать_доступ":
        await call.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='🔑 У кого заберём достум?',
            reply_markup=gen_access_markup(event)
        )
        await ev_helper.deny_access.set()
    elif call.data == "Назад":
        await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=f"🎖 Название: {event['event_title']}\n"
            f"📄 Описание: {event['event_description']}\n"
            f"🔗 Ссылка: {event['event_message_url']}\n",
        reply_markup=gen_event_markup(call.from_user.id, event)
    )
        await ev_helper.event.set()

@dp.message_handler(state=ev_helper.edit_access)
async def edit_access(message: types.Message, state: FSMContext):
    data = await state.get_data()
    event = data.get("event")
    await append_to_access(event['uuid'], message.text)
    new_event = await get_by_uuid(event['uuid'])
    await state.update_data(event=new_event)
    await dp.bot.delete_message(message_id=message.message_id,chat_id=message.from_user.id)
    if event is not None:
        await bot.send_message(
            chat_id=message.from_user.id,
            text=f"🎖 Название: {event['event_title']}\n"
                f"📄 Описание: {event['event_description']}\n"
                f"🔗 Ссылка: {event['event_message_url']}\n",
            reply_markup=gen_event_markup(message.from_user.id, event)
        )
    await ev_helper.event.set()

@dp.callback_query_handler(state=ev_helper.deny_access)
async def deny_access(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    event = data.get("event")
    if call.data != 'Назад':
        await deny_access_by_tg_id(call.data)
        await dp.bot.answer_callback_query(call.id)
        event = await get_by_uuid(event['uuid'])
        await state.update_data(event=event)
        await call.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='🔑 У кого заберём достум?',
            reply_markup=gen_access_markup(event)
        )
    elif call.data == "Назад":
        await call.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='Выбери пункт.',
            reply_markup=gen_edit_markup(event)
        )
        await ev_helper.editor.set()

@dp.message_handler(state=ev_helper.parser)
async def paper_receiver(message: types.Message, state: FSMContext):
    data = await state.get_data()
    event = data.get("event")
    message_id = data.get("message_id")
    a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_id,text=f'👷🏻‍♀️👨🏻‍🏭 Процесс:\n',parse_mode="HTML")
    url = message.text
    await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
    if url.startswith(('https://press.cheapshot.co')):
        a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_id,text=f'{a.text}\n- <em>Читаю газету...</em>',parse_mode="HTML")
        try:
            parser = Parser(url)
            enter_to_sheet = SheetsClient()
            result = await parser.parse()
            profile = await search_profile("tg_id", message.from_user.id)

            if profile['game_name'] == result['username'] or profile['role'] == 'creator':
                result['event_uuid'] = event['uuid']
                result['tg_id'] = message.from_user.id
                result['tg_username'] = message.from_user.username
                a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_id,text=f'{a.text}\n- <em>Регистрирую газету...</em>',parse_mode="HTML")
                paper = await reg_paper(result)
                if paper == True:
                    a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_id,text=f'{a.text}\n- <em>Вношу результат в таблицу...</em>\n',parse_mode="HTML")
                    await enter_to_sheet.insert_result(result)
                    a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_id,text=f'{a.text}\n- <em>✅ Газета зарегистрирована.</em>\n',reply_markup=gen_event_markup(message.from_user.id, event),parse_mode="HTML")
                else:
                    a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_id,text=f'{a.text}\n\n❌ Эта газета уже была зарегистрирована, нельзя использовать одну газету дважды.\n',reply_markup=gen_event_markup(message.from_user.id, event),parse_mode="HTML")
            else:
                a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_id,text=f'{a.text}\n\n❌ Нельзя использовать чужую газету.\n',reply_markup=gen_event_markup(message.from_user.id, event),parse_mode="HTML")
        except:
            a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_id,text=f'{a.text}\n\n🚨 Что-то пошло не так, попробуйте позже.\n',reply_markup=gen_event_markup(message.from_user.id, event),parse_mode="HTML")
    else:
        a = await bot.edit_message_text(chat_id=message.from_user.id, message_id=message_id,text=f'{a.text}\n\n🚨 Некорректный ввод.\n',reply_markup=gen_event_markup(message.from_user.id, event),parse_mode="HTML")
    
    await ev_helper.event.set()

async def return_popup_error(callid, errortype):
    await bot.answer_callback_query(callid, _('❌ Ошибка доступа: {errortype}').format(errortype=errortype), show_alert=True)

def gen_join_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(f"🆘 HOW TO?", callback_data='how_to'),
                InlineKeyboardButton(f"🏃🏻‍ Назад", callback_data='Назад'))
    return markup

def genmarkup(intended, data):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for i in data:
        markup.add(InlineKeyboardButton(f"{i['event_title'] if int(intended) != int(i['creator_tg_id']) else i['event_title'] + ' ⭐'}", callback_data=i['uuid']))
    return markup

def gen_edit_markup(event):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if event['type'] == 'clan_event':
        markup.add(InlineKeyboardButton(f"➕ Выдать доступ", callback_data='Выдать_доступ'),
                    InlineKeyboardButton(f"➖ Забрать доступ", callback_data='Забрать_доступ'))
    markup.add(InlineKeyboardButton(f"🏃🏻‍ Назад", callback_data='Назад'))
    return markup

def gen_event_markup(intended, event):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton(_("🎫 Участвовать"), callback_data="Участвовать"))
    if intended == event['creator_tg_id']:
        markup.add(InlineKeyboardButton(f"⚙ Редактировать", callback_data="Редактировать"))
    markup.add(InlineKeyboardButton(_("🏃🏻‍ Назад"), callback_data="Отменить"))
    return markup

def gen_access_markup(event):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    if event['access'] is not None:
        for i in event['access']:
            markup.add(InlineKeyboardButton(f"{i['game_name']} / {i['tg_id']}", callback_data=i['tg_id']))
    markup.add(InlineKeyboardButton(f"🏃🏻‍ Назад", callback_data='Назад'))
    return markup
                       