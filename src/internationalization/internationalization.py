from functools import wraps
import gettext

GETTEXT_DOMAIN = 'all_messages'
GETTEXT_DIR = 'src/internationalization/locales'

_ = gettext.gettext
spanish = gettext.translation(GETTEXT_DOMAIN, GETTEXT_DIR, languages=['es_ES'])
def set_translator(func):
    @wraps(func)
    def wrapped(bot, update, context, *pargs, **kwargs):
        if update.effective_user.language_code.startswith("es"):
            bot.change_translator(spanish.gettext)
        else:
            bot.change_translator(_)
        return func(bot, update, context, *pargs, **kwargs)
    return wrapped
