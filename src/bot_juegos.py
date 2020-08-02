#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

from bot_telegram import BotTelegram
from ahorcado.bot_ahorcado import BotTelegramAhorcado
from mastermind.bot_mastermind import BotMastermind
from buscaminas.bot_buscaminas import BotBuscaminas

# Para crear boton en telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json


class BotDeJuegosTelegram(BotTelegram):
    ESTADO_1, ESTADO_2 = 1, 2
    def __init__(self, nombre, token):
        BotTelegram.__init__(self, nombre, token)
        self.diccionario_de_juegos = {"ahorcado": BotTelegramAhorcado(), "buscaminas": BotBuscaminas(),
                                      "mastermind": BotMastermind()}
        self.estados = None
        try:
            with open('data.json', 'r') as datafile:
                self.datos_usuarios = json.load(datafile)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.datos_usuarios = {}
            with open('data.json', 'r') as datafile:
                json.dump(self.datos_usuarios, datafile)

    def start(self, update, context):
        bot = context.bot
        id_usuario = update.message.chat_id
        nombre_usuario = update.message.chat.first_name
        self.datos_usuarios[str(id_usuario)] = {"juego_actual": None, "estado": {}}
        with open('data.json', 'r+') as datafile:
            datafile.write(json.dumps(self.datos_usuarios))

        self.enviar_mensaje(bot, id_usuario, "Hola {}, bienvenido al bot de juegos. Utiliza /juegos para\
        ver la lista de juegos.".format(nombre_usuario))

    def juegos(self, update, context):

        opciones = [[InlineKeyboardButton(juego.capitalize(), callback_data=juego)] for juego in self.diccionario_de_juegos.keys()]

        update.message.reply_text('Los juegos disponibles son:', reply_markup=InlineKeyboardMarkup(opciones))
        return self.ESTADO_1

    def seleccionar_juego(self, update, context):
        # Datos que devuelve Telegram
        juego = update.callback_query.data
        usuario = update.callback_query.message.chat_id
        bot = context.bot
        try:
            self.datos_usuarios[str(usuario)]["juego_actual"] = juego
            with open('data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))
        except KeyError:
            self.datos_usuarios[str(usuario)] = {"juego_actual": juego}
            with open('data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))

        self.enviar_mensaje(bot, usuario, "Elegiste jugar al {}. Para cambiar de juego puedes usar /juegos nuevamente."\
                            .format(juego.capitalize()))

        self.diccionario_de_juegos[juego].jugar(update, context)

    def responder_boton_segun_juego(self, update, context):
        usuario = update.callback_query.message.chat_id
        juego = self.datos_usuarios[str(usuario)]["juego_actual"]
        self.diccionario_de_juegos[juego].responder_boton(update, context)

    def responder_mensaje_segun_juego(self, update, context):
        usuario = update.message.chat_id
        juego = self.datos_usuarios[str(usuario)]["juego_actual"]
        self.diccionario_de_juegos[juego].responder_mensaje(update, context)





