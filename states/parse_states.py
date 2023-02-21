from aiogram.dispatcher.filters.state import StatesGroup, State


class parse_paper(StatesGroup):
    paper = State()
    save = State()

