from aiogram.dispatcher.filters.state import StatesGroup, State


class create_event(StatesGroup):
    creator_tg_id = State()
    title = State()
    description = State()
    message_url = State()
    state = State()
    access = State()

