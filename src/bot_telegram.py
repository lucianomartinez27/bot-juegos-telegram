#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Librerias telegram
from telegram.ext import ApplicationBuilder, Updater, MessageHandler, CommandHandler,\
                         filters, CallbackQueryHandler, ConversationHandler,\
                         InlineQueryHandler

# Registro de actividades
import logging


class BotTelegram:

    def __init__(self, nombre, token):
        self.app = ApplicationBuilder().token(token).build()
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(nombre)

    def run(self):
        self.app.run_polling()

    async def enviar_mensaje(self, bot, id_usuario, mensaje, parse_mode=None) -> object:
        await bot.send_message(chat_id=id_usuario, text=mensaje, parse_mode=parse_mode)

    def handle_command(self, comando, callback):

        self.app.add_handler(CommandHandler(comando, callback))
          
    def handle_query(self, funcion, patron=None):
        self.app.add_handler(CallbackQueryHandler(funcion, pattern=patron))
    
    def handle_message(self, callback):
        mensaje_recibido = MessageHandler(filters.TEXT & (~filters.COMMAND), callback)
        self.app.add_handler(mensaje_recibido)

    def handle_inline_mode(self, comando, patron=None):
        self.app.add_handler(InlineQueryHandler(comando, pattern=patron))

    def generar_id_usuario(self, update):
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

    def generar_id_mensaje(self, update):
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