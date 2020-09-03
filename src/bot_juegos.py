#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

from src.bot_telegram import BotTelegram
from src.juegos.Ahorcado.bot_ahorcado import BotTelegramAhorcado
from src.juegos.Mastermind.bot_mastermind import BotMastermind
from src.juegos.Buscaminas.bot_buscaminas import BotBuscaminas
from src.juegos.TaTeTi.bot_tictactoe import BotTicTacToe
from src.juegos.TaTeTi_MultiPlayer.bot_tateti_inline import BotTaTeTiInLine
from src.utils.data_manager import DataManager
from telegram import InputTextMessageContent, InlineQueryResultArticle
from uuid import uuid4

import os

# Para crear boton en telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

bot_mastermind = BotMastermind()
bot_buscaminas = BotBuscaminas()
bot_tictactoe = BotTicTacToe()
bot_ahorcado = BotTelegramAhorcado()

bot_tateti_inline = BotTaTeTiInLine()


class BotDeJuegosTelegram(BotTelegram):
    def __init__(self, nombre, token):
        BotTelegram.__init__(self, nombre, token)
        self.decalogo_de_juegos = {bot_ahorcado.nombre(): bot_ahorcado,
                                   bot_buscaminas.nombre(): bot_buscaminas,
                                   bot_mastermind.nombre(): bot_mastermind,
                                   bot_tictactoe.nombre(): bot_tictactoe,
                                   bot_tateti_inline.nombre(): bot_tateti_inline}
        self.data_manager = DataManager(os.path.abspath(''))
        self.datos_usuarios = self.data_manager.generate_info(dict())

    def start(self, update, context):
        bot = context.bot
        id_usuario = self.generar_id_usuario(update)
        nombre_usuario = update.message.chat.first_name
        self.datos_usuarios[str(id_usuario)] = {"juego_actual": None, "estado": {}}
        self.data_manager.save_info(self.datos_usuarios)
        self.enviar_mensaje(bot, id_usuario, "Hola {}, bienvenido al bot de juegos. Utiliza /juegos para\
        ver la lista de juegos.".format(nombre_usuario))

    def mostrar_juegos(self, update, context):
        opciones = [[InlineKeyboardButton(juego.nombre(), callback_data=juego.nombre())] for juego in
                    self.decalogo_de_juegos.values() if not juego.es_inline()]
        update.message.reply_text('Los juegos disponibles son:', reply_markup=InlineKeyboardMarkup(opciones))
        self.logger.info("Se ha iniciado un nuevo juego")

    def mostrar_juegos_inline(self, update, context):
        resultados = []
        for juego in self.decalogo_de_juegos.values():
            if juego.es_inline():
                resultados.append((InlineQueryResultArticle(
                    id=uuid4(),
                    title=juego.nombre(),
                    input_message_content=InputTextMessageContent('Vamos a jugar a {}'.format(juego.nombre())),
                    reply_markup=juego.generar_markup(update, context))))
        id_usuario = self.generar_id_usuario(update)
        self.datos_usuarios[str(id_usuario)]['juego_actual'] = 'TaTeTi_MultiPlayer'
        self.data_manager.save_info(self.datos_usuarios)

        update.inline_query.answer(resultados)

    def seleccionar_juego(self, update, context):
        # Datos que devuelve Telegram
        juego = update.callback_query.data
        usuario = self.generar_id_usuario(update)
        bot = context.bot
        self.datos_usuarios[str(usuario)] = {"juego_actual": juego}
        self.data_manager.save_info(self.datos_usuarios)

        self.enviar_mensaje(bot, usuario, "Elegiste jugar al {}. Para cambiar de juego puedes usar /juegos nuevamente." \
                            .format(juego))

        self.decalogo_de_juegos[juego].jugar(update, context)

    def responder_boton_segun_juego(self, update, context):
        try:
            usuario = self.generar_id_usuario(update)
            juego = self.datos_usuarios[str(usuario)]["juego_actual"]
            self.decalogo_de_juegos[juego].responder_boton(update, context)
        except KeyError:
            # Solucionar luego este hardcodeo
            self.decalogo_de_juegos['TaTeTi_MultiPlayer'].responder_boton(update, context)

    def responder_mensaje_segun_juego(self, update, context):
        usuario = self.generar_id_usuario(update)
        juego = self.datos_usuarios[str(usuario)]["juego_actual"]
        self.decalogo_de_juegos[juego].responder_mensaje(update, context)

