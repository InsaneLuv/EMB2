from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from database.events import event_reg
from filters import AdminCommand
from loader import dp
from states import create_event
from utils.misc import rate_limit


@rate_limit(limit=3600)
@dp.callback_query_handler(AdminCommand(),text="Создать1")
async def event_creator(call: CallbackQuery):
    await call.bot.send_message(chat_id=call.from_user.id, text='🎖 Как назовём ивент?\n'
                                                                '(Это название будет видно пользователям)')
    await create_event.title.set()


@dp.message_handler(state=create_event.title)
async def state1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(creator_tg_id=message.from_user.id)
    await state.update_data(title=answer)
    await message.reply("📄 Описание ивента")

    await create_event.description.set()


@dp.message_handler(state=create_event.description)
async def state2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(description=answer)
    await message.reply("🔗 Ссылка на сообщение")

    await create_event.message_url.set()


@dp.message_handler(state=create_event.message_url)
async def state3(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(message_url=answer)
    await state.update_data(state="True")
    await state.update_data(access="*")
    
    data = await state.get_data()
    title = data.get("title")
    description = data.get("description")
    message_url = data.get("message_url")
    creator = data.get("creator_tg_id")

    await message.reply("✅ Ивент создан\n\n"
                        f"🎖 Название: {title}\n"
                        f"📄 Описание: {description}\n"
                        f'🔗 Ссылка: {message_url}\n'
                        f'📣 Организатор:  <a href="tg://user?id={creator}">Ссылка</a>', parse_mode='HTML')
    await event_reg(state)
    await state.finish()
