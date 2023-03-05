import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, location, ContentTypes

from data.config import admins
from database import profile_reg, search_profile
from database.profile.profile import update_adress
from filters import IsSubscriber
from keyboards.inline import registration_ikb_menu, yes_no_ikb_menu
from loader import dp, bot, _
from states import reger
from tools.parse_tool_clan.paper_parser_clan import paper_parse_clan
from utils.misc import rate_limit


@rate_limit(limit=2)
@dp.message_handler(IsSubscriber(), lambda message: "👤" in message.text)
async def button_profile_react(message: types.Message):
    profile_info = await search_profile("tg_id",message.from_user.id)

    if profile_info != None:
        await bot.send_message(chat_id=message.from_user.id, text=
                                 'Ваш профиль:\n'
                                f'🆔: {profile_info["tg_id"]}\n'
                                f'👤: {profile_info["game_name"]}\n'
                                f'💼: {profile_info["role"]}\n'
                                f'💰: {profile_info["adress"]}', reply_markup=edit_profile())
    else:
        await message.reply(_('👤 Ваш профиль не найден, пройти регистрацию?'),reply_markup=registration_ikb_menu)


@dp.callback_query_handler(text="Отменить")
async def disabler(call: CallbackQuery):
    await bot.delete_message(message_id=call.message.from_user.id, chat_id=call.from_user.id)


@dp.callback_query_handler(text="Пройти")
async def event_creator(call: CallbackQuery):
    await call.bot.send_message(chat_id=call.from_user.id, text=_('👤 Отправь ЛЮБУЮ свою газету с акутальным внутриигровым ником.\n'
                                                                '(Использование чужой газеты наказуемо)'))
    await reger.tg_id.set()

@dp.callback_query_handler(text="bounty_adress")
async def bounty(call: CallbackQuery, state: FSMContext):
    await state.update_data(message_id=call.message.message_id)
    await call.bot.edit_message_text(message_id=call.message.message_id, chat_id=call.from_user.id, text=_('💰 Отправьте вашу геопозицию:\n1. 📎 Прикрепить.\n2. 📍 Геопозиция.\n3. 📍 Отправить геопозицию.'))
    await reger.geopos.set()


@dp.message_handler(content_types=ContentTypes.ANY, state=reger.geopos)
async def state2_reg(message: types.Message, state: FSMContext):
    profile_info = await search_profile("tg_id",message.from_user.id)
    data = await state.get_data()
    msgid = data.get("message_id")
    try:
        url = f'csx://location?lat={message.location.latitude}&lng={message.location.longitude}'
        await update_adress(url, profile_info['tg_id'])
        await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
        profile_info = await search_profile("tg_id",message.from_user.id)
        await bot.edit_message_text(message_id=msgid, chat_id=message.from_user.id,
                                    text=
                                    '🥳 Профиль обновлён!\n'
                                    f'🆔: {profile_info["tg_id"]}\n'
                                    f'👤: {profile_info["game_name"]}\n'
                                    f'💼: {profile_info["role"]}\n'
                                    f'💰: {profile_info["adress"]}', reply_markup=edit_profile())
    except:
        await bot.delete_message(message_id=message.message_id, chat_id=message.from_user.id)
        await bot.edit_message_text(message_id=msgid, chat_id=message.from_user.id,
                            text=
                            '❌ Профиль не обновлён.\n'
                            f'🆔: {profile_info["tg_id"]}\n'
                            f'👤: {profile_info["game_name"]}\n'
                            f'💼: {profile_info["role"]}\n'
                            f'💰: {profile_info["adress"]}', reply_markup=edit_profile())
    CancelHandler()
    await state.finish()



@dp.message_handler(state=reger.tg_id)
async def state1_reg(message: types.Message, state: FSMContext):
    answer = message.text

    if answer == "zxc":
        answer = "https://press.cheapshot.co/view.html?id=ddb27ad5713275159e522e8a3d909252%2F98ce05f52e8fca5f9ff2e3747d76dc84"

    if not answer.startswith(('https://press.cheapshot.co', 'http://press.cheapshot.co', 'press.cheapshot.co')):
        await bot.send_message(chat_id=message.from_user.id, text='🚨 Действие отменено\n'
                                                                  '(Некорректная ссылка)')
        CancelHandler()
        await state.finish()
    else:
        result = await paper_parse_clan(answer, "registration")
        await message.reply(f"Вы - {result['username']}?",reply_markup=yes_no_ikb_menu)
        await state.update_data(tg_id=message.from_user.id)
        await state.update_data(name_from_paper=result['username'])

    await reger.next()


@dp.callback_query_handler(state=reger.name_from_paper)
async def call1(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name_from_paper = data.get("name_from_paper")
    if call.data == "Да":
        profile_info = await search_profile("game_name",name_from_paper)
        if profile_info is None:
            if int(call.from_user.id) in admins:
                await state.update_data(role="creator")
            else:
                await state.update_data(role="user")

            await state.update_data(adress='None')
            await state.update_data(unique='None')
            await profile_reg(state)
            profile_info = await search_profile("tg_id", call.from_user.id)
            await bot.send_message(chat_id=call.from_user.id, text=f'Ok')
            CancelHandler()
            await state.finish()
        else:
            await bot.send_message(call.from_user.id, text=_('👤 На этот никнейм уже была произведена регистрация'))
            CancelHandler()
            await state.finish()
        await call.message.delete()
    else:
        CancelHandler()
        await state.finish()
        await call.message.delete()


def edit_profile():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton(f"Set 💰 Bounty adress", callback_data='bounty_adress'))
    return markup