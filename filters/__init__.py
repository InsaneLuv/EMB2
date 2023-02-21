from aiogram import Dispatcher

from .chat_subscriber import IsSubscriber
from .private_chat import IsPrivate
from .admincommand import AdminCommand


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(IsSubscriber)
    dp.filters_factory.bind(AdminCommand)