#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Librerias telegram
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler,\
                         filters, CallbackQueryHandler, \
                         InlineQueryHandler

# Registro de actividades
import logging
from internationalization import _


class BotTelegram:

    def __init__(self, name, token):
        self._ = None
        self.language = 'en'
        self.name = name
        self.logger = logging.getLogger(name)
        self.app = ApplicationBuilder().token(token).build()
        self.app.add_error_handler(self.error_handler)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    async def error_handler(self, update, context):
        """Log the error and send a telegram message to notify the developer."""
        self.logger.error(msg="Exception while handling an update:", exc_info=context.error)

    def initialize_translator(self):
        self._ = _
        self.language = 'en'
        
    def change_translator(self, new_translator, language_code):
        self._ = new_translator
        self.language = language_code

    def run_polling(self):
        self.app.run_polling()

    def run_webhook(self, url, port, url_path, secret_token=None, cert=None, key=None):
        self.app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=url_path,
            webhook_url=f"{url}/{secret_token if secret_token else ''}",
            cert=cert,
            key=key,
            secret_token=secret_token
        )

    def run(self):
        self.run_polling()

    async def send_message(self, bot, user_id, message, parse_mode=None, reply_markup=None) -> object:
        try:
            return await bot.send_message(chat_id=user_id, text=message, parse_mode=parse_mode, reply_markup=reply_markup)
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            raise e

    async def edit_message_text(self, bot, chat_id, message_id, text, parse_mode=None, reply_markup=None):
        try:
            return await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode=parse_mode, reply_markup=reply_markup)
        except Exception as e:
            self.logger.error(f"Error editing message text: {e}")
            raise e

    async def edit_message_reply_markup(self, bot, chat_id, message_id, reply_markup=None):
        try:
            return await bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=reply_markup)
        except Exception as e:
            self.logger.error(f"Error editing message reply markup: {e}")
            raise e

    def handle_command(self, comando, callback):

        self.app.add_handler(CommandHandler(comando, callback))
          
    def handle_query(self, funcion, patron=None):
        self.app.add_handler(CallbackQueryHandler(funcion, pattern=patron))
    
    def handle_message(self, callback):
        mensaje_recibido = MessageHandler(filters.TEXT & (~filters.COMMAND), callback)
        self.app.add_handler(mensaje_recibido)

    def handle_inline_mode(self, comando, patron=None):
        self.app.add_handler(InlineQueryHandler(comando, pattern=patron))

    def get_user_id(self, update):
        return update.effective_user.id

    def get_chat_id(self, update):
        return update.effective_chat.id

    def get_message_id(self, update):
        if update.callback_query and update.callback_query.inline_message_id:
            return update.callback_query.inline_message_id
        return update.effective_message.message_id
