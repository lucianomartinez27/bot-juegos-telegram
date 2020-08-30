#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

from src.bot_telegram import BotTelegram
from src.utils.data_manager import DataManager
import os


class BotBase(BotTelegram):

    def __init__(self):
        self.data_manager = DataManager(os.path.abspath(''))
        self.datos_usuarios = self.data_manager.generate_info(dict())


    def no_entiendo_mensaje(self):
        return "Disculpa, no entiendo tu mensaje."

    def responder_mensaje(self, update, context):
        usuario = update.message.chat_id
        bot = context.bot
        self.enviar_mensaje(bot, usuario, self.no_entiendo_mensaje())

    def responder_boton(self, update, context):
        usuario = update.callback_query.message.chat_id
        bot = context.bot
        self.enviar_mensaje(bot, usuario, self.no_entiendo_mensaje())