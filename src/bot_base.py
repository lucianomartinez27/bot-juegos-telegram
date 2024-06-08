#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import os
from bot_telegram import BotTelegram
from utils.data_manager import DataManager


class BotBase(BotTelegram):

    def __init__(self, file):
        self.data_manager = DataManager(os.path.dirname(file))
        self.datos_usuarios = self.data_manager.generate_info(dict())

    def es_inline(self):
        return False

    def no_entiendo_mensaje(self):
        return "Disculpa, no entiendo tu mensaje."

    async def responder_mensaje(self, update, context):
        usuario = self.generar_id_usuario(update)
        bot = context.bot
        await self.enviar_mensaje(bot, usuario, self.no_entiendo_mensaje())

    async def responder_boton(self, update, context):
        usuario = self.generar_id_usuario(update)
        bot = context.bot
        await self.enviar_mensaje(bot, usuario, self.no_entiendo_mensaje())