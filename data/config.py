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

settings = [
    's_police', 's_police_heli', 's_police_car', 's_ordinary', 's_dragon', 's_pdragon', 's_alien','s_rat'
]

technical_messages = {

    'bot_start': "🚀 Бот перезапущен.\n(Техническое уведомление)",

    'commands': "1. /start - 💡 Start command, 🇷🇺➰🇬🇧 Switch language.",

    'For_what': "🔩 Для твоего удобства ❤️.",

    'right_title_example': "[CLAN-WARS] - @cheapshotevent\n" \
                           "[ALIEN-GENOCIDE] - @cheapshothumor",
    
    'special': '- @Yankeees and "CLAN EVENTS" for cooperation and using bot in their events.\n' \
               '- @itcig and his service "cheapshot.app" for providing up-to-date information about the monuments.\n\n' \
               '- And to Everyone who invited their friends to the bot group, thank you for your support ❤️.'
                           
}


urls = {
    'creator': "https://t.me/spaghetti_coder"
}

papers = [
    'https://press.cheapshot.co/view.html?id=a020bce4507ba234c9a736a825447bde/e4d5d18d39d432cbe3647087bae3e088',
    'https://press.cheapshot.co/view.html?id=d42f30b0c5d3976cacf1294ebdb94ed5/d99c713d25e57f181c5b5bb6894254a1',
    'https://press.cheapshot.co/view.html?id=614e7762dfba2a86974f6a79df8cb3b3/749829ce40801a69062afe13f8d4213e',
    'https://press.cheapshot.co/view.html?id=c902646d3ac69eaf79ac0cb7e9f0e0a4/65f5fb1d7d10faefe463c65574fdef15',
    'https://press.cheapshot.co/view.html?id=d8fefc8faa24b82d30f64fd364fad2dd/3c6b0fd8043a823f7a1dc4a0076de72b',
    'https://press.cheapshot.co/view.html?id=8ebc4ddffa84d1c4f47e12a5a8732bf1/11f081daa1c825d460a483a7cdb17b9e',
    'https://press.cheapshot.co/view.html?id=20966a6f53f5bca88f334be9c0646ec3/0000532217cd33cf524ffc63d370eb93',
    'https://press.cheapshot.co/view.html?id=78c8df4ba308794b81f8ba3150abc7e0/be015ec7d8831c884be7ec5136f9c9a5',
    'https://press.cheapshot.co/view.html?id=a2cdf9e1e22d969a33831dfd6dc7dff2/9b523c20eaec6030525ada0dd83f1e1d',
    'https://press.cheapshot.co/view.html?id=269b8294171dbac52a0872068e40eb76/52a56a8c62caa8d527927aca9aaf2575'
]

test_paper = {
    1: f'{papers[0]}',
    2: f'{papers[0]},{papers[1]}',
    3: f'{papers[0]},{papers[1]},{papers[2]}',
    4: f'{papers[0]},{papers[1]},{papers[2]},{papers[3]}',
    5: f'{papers[0]},{papers[1]},{papers[2]},{papers[3]},{papers[4]}',
    6: f'{papers[0]},{papers[1]},{papers[2]},{papers[3]},{papers[4]},{papers[5]}',
    7: f'{papers[0]},{papers[1]},{papers[2]},{papers[3]},{papers[4]},{papers[5]},{papers[6]}',
    8: f'{papers[0]},{papers[1]},{papers[2]},{papers[3]},{papers[4]},{papers[5]},{papers[6]},{papers[7]}',
    9: f'{papers[0]},{papers[1]},{papers[2]},{papers[3]},{papers[4]},{papers[5]},{papers[6]},{papers[7]},{papers[8]}',
    10: f'{papers[0]},{papers[1]},{papers[2]},{papers[3]},{papers[4]},{papers[5]},{papers[6]},{papers[7]},{papers[8]},{papers[9]}',
}