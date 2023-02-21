from typing import Tuple, Any

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from data.config import I18N_DOMAIN, BASE_DIR, LOCALES_DIR
from database.profile.profile import search_lang


async def get_lang(user_id):
    lang = await search_lang(user_id)    
    return lang      


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Any) -> str:
        user = types.User.get_current()
        try:
            return await get_lang(user.id) 
        except:
            return user.language_code

def setup_multilanguage(dp):
    i18n = ACLMiddleware(I18N_DOMAIN,LOCALES_DIR)
    dp.middleware.setup(i18n)
    return i18n