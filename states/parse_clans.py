from aiogram.dispatcher.filters.state import StatesGroup, State


class parse_paper_clan(StatesGroup):
    paper_clan = State()
    save_clan = State()

