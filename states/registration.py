from aiogram.dispatcher.filters.state import StatesGroup, State


class reger(StatesGroup):
    tg_id = State()
    name_from_paper = State()
    role = State()

