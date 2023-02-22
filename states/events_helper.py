from aiogram.dispatcher.filters.state import StatesGroup, State


class ev_helper(StatesGroup):
    event = State()
    editor = State()
    edit_title = State()
    edit_desc = State()
    edit_url = State()
    edit_state = State()
    edit_access = State()
    edit_psettings = State()

