from functools import wraps
import gettext

GETTEXT_DOMAIN = 'all_messages'
GETTEXT_DIR = 'src/internationalization/locale'

_ = gettext.gettext
spanish = gettext.translation(GETTEXT_DOMAIN, GETTEXT_DIR, languages=['es_ES'], fallback=True)

def set_translator(func):
    @wraps(func)
    async def wrapped(self, update, context, *pargs, **kwargs):
        user_id = str(self.get_user_id(update))
        # Determine language from user preferences or fallback to Telegram's language_code
        user_lang = self.user_data.get(user_id, {}).get("language")
        
        if not user_lang and update.effective_user:
            user_lang = update.effective_user.language_code

        if user_lang and user_lang.startswith("es"):
            new_translator = spanish.gettext
            lang_code = "es"
        else:
            new_translator = _
            lang_code = "en"
        
        self.change_translator(new_translator, lang_code)
            
        return await func(self, update, context, *pargs, **kwargs)
    return wrapped
