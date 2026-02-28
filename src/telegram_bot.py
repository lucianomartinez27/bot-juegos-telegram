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
        self.app = ApplicationBuilder().token(token).build()
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(name)

    def initialize_translator(self):
        self._ = _
        self.language = 'en'
        
    def change_translator(self, new_translator, language_code):
        self._ = new_translator
        self.language = language_code

    def run(self):
        self.app.run_polling()

    async def send_message(self, bot, user_id, message, parse_mode=None, reply_markup=None) -> object:
        await bot.send_message(chat_id=user_id, text=message, parse_mode=parse_mode, reply_markup=reply_markup)

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
        try:
            id = update.callback_query.message.chat_id
        except:
            try:
                id = update.message.chat_id
            except:
                try:
                    id = update.inline_query.from_user.id
                except:
                    id = update.callback_query.from_user.id
        return id

    def get_message_id(self, update):
        try:
            id = update.callback_query.message.message_id
        except:
            try:
                id = update.message.message_id
            except:
                try:
                    id = update.inline_query.from_user.message_id
                except:
                    id = update.callback_query.inline_message_id
        return id