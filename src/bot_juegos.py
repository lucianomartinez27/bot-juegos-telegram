#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

from src.bot_telegram import BotTelegram
from src.ahorcado.bot_ahorcado import BotTelegramAhorcado
from src.mastermind.bot_mastermind import BotMastermind
from src.buscaminas.bot_buscaminas import BotBuscaminas
from src.tic_tac_toe.bot_tictactoe import BotTicTacToe
from src.utils.data_manager import DataManager
import os

# Para crear boton en telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json


class BotDeJuegosTelegram(BotTelegram):
    def __init__(self, nombre, token):
        BotTelegram.__init__(self, nombre, token)
        self.decalogo_de_juegos = {"ahorcado": BotTelegramAhorcado(), "buscaminas": BotBuscaminas(),
                                   "mastermind": BotMastermind(), "Ta-Te-Ti": BotTicTacToe()}
        self.data_manager = DataManager(os.path.abspath(''))
        self.datos_usuarios = self.data_manager.generate_info(dict())

    def start(self, update, context):
        bot = context.bot
        id_usuario = update.message.chat_id
        nombre_usuario = update.message.chat.first_name
        self.logger.info("Se ha iniciado un nuevo usuario. ID: {}. Nombre: {}".format(id_usuario, nombre_usuario))
        self.datos_usuarios[str(id_usuario)] = {"juego_actual": None, "estado": {}}
        self.data_manager.save_info(self.datos_usuarios)

        self.enviar_mensaje(bot, id_usuario, "Hola {}, bienvenido al bot de juegos. Utiliza /juegos para\
        ver la lista de juegos.".format(nombre_usuario))

    def mostrar_juegos(self, update, context):

        opciones = [[InlineKeyboardButton(juego.capitalize(), callback_data=juego)] for juego in
                    self.decalogo_de_juegos.keys()]

        update.message.reply_text('Los juegos disponibles son:', reply_markup=InlineKeyboardMarkup(opciones))
        self.logger.info("Se ha iniciado un nuevo juego")

    def seleccionar_juego(self, update, context):
        # Datos que devuelve Telegram
        juego = update.callback_query.data
        usuario = update.callback_query.message.chat_id
        bot = context.bot
        try:
            self.datos_usuarios[str(usuario)]["juego_actual"] = juego
            self.data_manager.save_info(self.datos_usuarios)
        except KeyError:
            self.datos_usuarios[str(usuario)] = {"juego_actual": juego}
            self.data_manager.save_info(self.datos_usuarios)

        self.enviar_mensaje(bot, usuario, "Elegiste jugar al {}. Para cambiar de juego puedes usar /juegos nuevamente." \
                            .format(juego.capitalize()))

        self.decalogo_de_juegos[juego].jugar(update, context)

    def responder_boton_segun_juego(self, update, context):
        usuario = update.callback_query.message.chat_id
        juego = self.datos_usuarios[str(usuario)]["juego_actual"]
        self.decalogo_de_juegos[juego].responder_boton(update, context)

    def responder_mensaje_segun_juego(self, update, context):
        usuario = update.message.chat_id
        juego = self.datos_usuarios[str(usuario)]["juego_actual"]
        self.decalogo_de_juegos[juego].responder_mensaje(update, context)



