import logging
import re
import traceback
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, location, ContentTypes
from aiogram import md
from data.config import admins
from database import profile_reg, search_profile
from database.profile.profile import get_profile_settings_cd, set_profile_settings_cd, update_address
from filters import IsSubscriber
from keyboards.inline import registration_ikb_menu, yes_no_ikb_menu
from loader import dp, bot, _
from states import reger
from tools.parse_other.parser import Parser
from tools.parse_tool_clan.paper_parser_clan import paper_parse_clan
from utils.misc import rate_limit
from datetime import datetime, timedelta


@rate_limit(limit=2)
@dp.message_handler(IsSubscriber(), lambda message: "👤" in message.text)
async def button_profile_react(message: types.Message, state: FSMContext):
    profile_info = await search_profile("tg_id",message.from_user.id)
    if profile_info != None:
        profile_out = await get_profile_out(message.from_user.id)
        await bot.send_message(chat_id=message.from_user.id, text=_('Ваш профиль:\n {profile_out}').format(profile_out=profile_out), reply_markup=edit_profile(),parse_mode="HTML")
    else:
        a = await bot.send_message(chat_id=message.from_user.id, text=_('👤 Ваш профиль не найден, пройти регистрацию?'),reply_markup=registration_ikb_menu)
        await state.update_data(message_id=a.message_id)

@dp.callback_query_handler(text="Отменить")
async def disabler2(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msgid = data.get("message_id")
    await bot.delete_message(message_id=msgid, chat_id=call.from_user.id)

@dp.callback_query_handler(text="Пройти")
async def event_creator(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msgid = data.get("message_id")
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=msgid,
                                text=_('👤 Отправь свою газету с актуальным внутриигровым ником.\n(Дата газета не важна, важнен никнейм.)'))
    await reger.tg_id.set()

@dp.callback_query_handler(text="help_bounty", state='*')
async def disabler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msgid = data.get("message_id")
    try:
        a = await bot.send_document(call.from_user.id,
                            document='https://s2.gifyu.com/images/IMG_2866.gif', parse_mode="HTML")
        await state.update_data(help_message_id=a.message_id)
    except:
        pass
    

def help():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(_("🆘 Помощь"), callback_data='help_bounty'))
    return markup

@dp.callback_query_handler(text="bounty_address")
async def bounty(call: CallbackQuery, state: FSMContext):
    await state.update_data(message_id=call.message.message_id)
    data = await state.get_data()
    msgid = data.get("message_id")
    profile_info = await search_profile("tg_id",call.from_user.id)
    cooldown = await get_profile_settings_cd(call.from_user.id)
    input_datetime = datetime.strptime(str(cooldown['bounty_cd']), '%Y-%m-%d')
    current_datetime = datetime.now()
    if input_datetime >= current_datetime:
        await bot.answer_callback_query(call.id, _('Изменение будет доступно: {input_date}').format(input_date=str(input_datetime), show_alert=True))
        try:
            profile_out = await get_profile_out(call.from_user.id)
            await bot.edit_message_text(message_id=msgid, chat_id=call.from_user.id,
                            text='⏱ Editing on cooldown.\n'
                            f'{profile_out}', reply_markup=edit_profile(),parse_mode="HTML")
        except:
            pass
        CancelHandler()
        await state.finish()
    else:
        await call.bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=_('💰 Отправьте вашу геопозицию:\n1. 📎 Прикрепить.\n2. 📍 Геопозиция.\n3. 📍 Отправить геопозицию.\n\n(Следуюшее изменение будет доступно через 3 дня)'),reply_markup=help())
        await reger.geopos.set()

@dp.message_handler(content_types=ContentTypes.ANY, state=reger.geopos)
async def state2_reg(message: types.Message, state: FSMContext):
    profile_info = await search_profile("tg_id",message.from_user.id)
    profile_out = await get_profile_out(message.from_user.id)
    data = await state.get_data()
    msgid = data.get("message_id")
    help_msg_id = data.get("help_message_id")
    try:
        await bot.delete_message(chat_id=message.from_user.id, message_id=help_msg_id)
    except:
        pass
    if str(message.content_type) == 'location':
        try:
            url = f'csx://location?lat={message.location.latitude}&lng={message.location.longitude}'
            await update_address(url, profile_info['tg_id'])
            cd_date = (datetime.now()+timedelta(days=3))
            await set_profile_settings_cd('bounty_cd', profile_info['tg_id'], cd_date.strftime("%Y-%m-%d"))
            await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
            profile_out = await get_profile_out(message.from_user.id)
            await bot.edit_message_text(message_id=msgid, chat_id=message.from_user.id,
                                        text=
                                        '🥳 Profile updated!\n'
                                        f'{profile_out}', reply_markup=edit_profile(),parse_mode="HTML")
        except Exception as e:
            logging.warning(e)
            await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
            await bot.edit_message_text(message_id=msgid, chat_id=message.from_user.id,
                                text=
                                '❌ Error while updating.\n'
                                f'{profile_out}', reply_markup=edit_profile(),parse_mode="HTML")
        CancelHandler()
        await state.finish()
    else:
        await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
        await bot.edit_message_text(message_id=msgid, chat_id=message.from_user.id,
                                text=
                                '❌ Incorrect input.\n'
                                f'{profile_out}', reply_markup=edit_profile(),parse_mode="HTML")
        CancelHandler()
        await state.finish()

async def get_profile_out(tg_id):
    profile_info = await search_profile("tg_id",tg_id)
    output = f'🆔: <code>{md.quote_html(profile_info["tg_id"])}</code>\n' \
             f'👤: <code>{md.quote_html(profile_info["game_name"])}</code>\n' \
             f'💼: {md.quote_html(profile_info["role"])}\n' \
             f'💰: <code>{md.quote_html(profile_info["address"])}</code>'
    return output

@dp.message_handler(state=reger.tg_id)
async def state1_reg(message: types.Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()
    msgid = data.get("message_id")
    await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
    try:
        if answer == "zxc":
            answer = "https://press.cheapshot.co/view.html?id=ddb27ad5713275159e522e8a3d909252%2F98ce05f52e8fca5f9ff2e3747d76dc84"
        if not answer.startswith(('https://press.cheapshot.co', 'http://press.cheapshot.co', 'press.cheapshot.co')):
            await bot.edit_message_text(message_id=msgid, chat_id=message.from_user.id,text='🚨 Действие отменено\n(Некорректная ссылка)')
            CancelHandler()
            await state.finish()
        else:
            answer = re.sub('&inapp=true', '', answer)
            await bot.edit_message_text(message_id=msgid, chat_id=message.from_user.id,text=f"🕵🏻‍♂️ Читаю газету...")
            parser = Parser(answer)
            result = await parser.parse()
            username = str(result['username'])
            await bot.edit_message_text(message_id=msgid, chat_id=message.from_user.id,text=f"Вы - `{username}`?",reply_markup=yes_no_ikb_menu, parse_mode='HTML')
            await state.update_data(tg_id=message.from_user.id)
            await state.update_data(name_from_paper=result['username'])
            await reger.next()
    except Exception:
        e = traceback.format_exc()
        logging.warning(e)
        await bot.edit_message_text(message_id=msgid, chat_id=message.from_user.id,text='🚨 Действие отменено\n(Ошибка операции)')
        CancelHandler()
        await state.finish()

@dp.callback_query_handler(state=reger.name_from_paper)
async def call1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    msgid = data.get("message_id")
    name_from_paper = data.get("name_from_paper")
    if call.data == "Да":
        profile = await search_profile('game_name',name_from_paper)
        if profile is None:
            if call.from_user.id in admins:
                role = 'creator'
            else:
                role = 'user'
            profile = {
                'tg_id': call.from_user.id,
                'game_name': name_from_paper,
                'role': role,
                'address': 'None',
                'unique': 'None'
            }
            await profile_reg(profile)
            profile_info = await search_profile("tg_id", call.from_user.id)
            output = f'🆔: <code>{md.quote_html(profile_info["tg_id"])}</code>\n' \
             f'👤: <code>{md.quote_html(profile_info["game_name"])}</code>\n' \
             f'💼: {md.quote_html(profile_info["role"])}\n' \
             f'💰: <code>{md.quote_html(profile_info["address"])}</code>'
            await bot.edit_message_text(message_id=msgid, chat_id=call.from_user.id,
                                    text=
                                    '🥳 Профиль обновлён!\n'
                                    f'{output}', reply_markup=edit_profile(), parse_mode='HTML')
            CancelHandler()
            await state.finish()
        else:
            await bot.edit_message_text(message_id=msgid, chat_id=call.from_user.id,text=_('👤 На этот никнейм уже была произведена регистрация'))
            CancelHandler()
            await state.finish()
    else:
        CancelHandler()
        await state.finish()
        await call.message.delete()

def edit_profile():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(f"Set 💰 Bounty address", callback_data='bounty_address'))
    return markup
