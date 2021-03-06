#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

from src.bot_telegram import BotTelegram
from src.utils.data_manager import DataManager


class BotBase(BotTelegram):

    def __init__(self, path):
        self.data_manager = DataManager(path)
        self.datos_usuarios = self.data_manager.generate_info(dict())

    def es_inline(self):
        return False

    def no_entiendo_mensaje(self):
        return "Disculpa, no entiendo tu mensaje."

    def responder_mensaje(self, update, context):
        usuario = self.generar_id_usuario(update)
        bot = context.bot
        self.enviar_mensaje(bot, usuario, self.no_entiendo_mensaje())

    def responder_boton(self, update, context):
        usuario = self.generar_id_usuario(update)
        bot = context.bot
        self.enviar_mensaje(bot, usuario, self.no_entiendo_mensaje())