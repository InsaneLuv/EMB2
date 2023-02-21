from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import CallbackQuery

from data.config import admins
from database import profile_reg, search_profile
from filters import IsSubscriber, AdminCommand
from keyboards.inline import registration_ikb_menu, yes_no_ikb_menu, tester_ikb_menu
from loader import dp, bot
from states import reger
from tools.parse_tool_clan.paper_parser_clan import paper_parse_clan
from utils.misc import rate_limit


@rate_limit(limit=2)
@dp.message_handler(AdminCommand(),lambda message: "👽" in message.text)
async def tester_react(message: types.Message):
    a = await bot.send_message(chat_id=message.from_user.id, text=f'Test menu, choose test', reply_markup=tester_ikb_menu)