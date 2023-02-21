import datetime
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

now = datetime.datetime.now()
now = now.strftime("%d-%m-%Y %H:%M")

I18N_DOMAIN = 'domain'
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / 'locales'

# 465989596
admins = [
    465989596,
    632473665
]

# -1001846244670

chat_ids = [
    -1001846244670
]


technical_messages = {

    'bot_start': "🚀 Бот перезапущен.\n(Техническое уведомление)",

    'commands': "1. /start\n"
                "\n",

    'For_what': "🔩 Бот разрабатывается для помощи контент-мейкерам в проведении ивентов, а так же игрокам для комфортного участия в них.",

    'right_title_example': "[CLAN-WARS] - @cheapshotevent\n" \
                           "[ALIEN-GENOCIDE] - @cheapshothumor"
}


urls = {
    'creator': "https://t.me/spaghetti_coder"
}