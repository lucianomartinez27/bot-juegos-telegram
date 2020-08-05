#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.bot_telegram import BotTelegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from .funciones import crear_tablero, despejar_tablero, tablero_visible_inicial, verificar_tablero, descubrir_tablero
import json


class BotBuscaminas(BotTelegram):
    def __init__(self):
        self.datos_usuarios = {}
        try:
            with open('buscaminas/data.json', 'r+') as datafile:
                self.datos_usuarios = json.load(datafile)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open('buscaminas/data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))

    def generar_datos(self, id_usuario):
        # id_usuario se convierte en string porque las claves json deben ser de ese tipo
        self.datos_usuarios[str(id_usuario)] = {}
        bombas = self.datos_usuarios[str(id_usuario)]['bombas'] = 10
        t_oculto = self.datos_usuarios[str(id_usuario)]['tablero_oculto'] = crear_tablero(8, 8, bombas)
        self.datos_usuarios[str(id_usuario)]['tablero_visible'] = tablero_visible_inicial(t_oculto)
        self.datos_usuarios[str(id_usuario)]['partida_terminada'] = False
        with open('buscaminas/data.json', 'w') as datafile:
            datafile.write(json.dumps(self.datos_usuarios))

    def jugar(self, update, context):
        id_usuario = update.callback_query.message.chat_id
        self.generar_datos(id_usuario)
        tablero = self.datos_usuarios[str(id_usuario)]['tablero_visible']

        opciones = [[InlineKeyboardButton(tablero[i][j], callback_data="{} {}".format(i, j))
                     for j in range(len(tablero[0]))] for i in range(len(tablero))]

        update.callback_query.message.reply_text('Buscaminas:', reply_markup=InlineKeyboardMarkup(opciones))

    def responder_boton(self, update, context):
        x, y = update.callback_query.data.split()
        bot = context.bot
        id_usuario = update.callback_query.message.chat.id
        id_mensaje = update.callback_query.message.message_id
        t_oculto = self.datos_usuarios[str(id_usuario)]['tablero_oculto']
        t_visible = self.datos_usuarios[str(id_usuario)]['tablero_visible']
        bombas = self.datos_usuarios[str(id_usuario)]['bombas']
        partida_terminada = self.datos_usuarios[str(id_usuario)]['partida_terminada']
        if not partida_terminada:
            despejar_tablero(int(x), int(y), t_oculto, t_visible)
            if t_oculto[int(x)][int(y)] == 9:
                self.enviar_mensaje(bot, id_usuario, "perdiste bobo")
                descubrir_tablero(t_visible, t_oculto)
                self.datos_usuarios[str(id_usuario)]['partida_terminada'] = True
            if verificar_tablero(t_visible, bombas):
                descubrir_tablero(t_visible, t_oculto)
                self.enviar_mensaje(bot, id_usuario, "ganaste bobo")
                self.datos_usuarios[str(id_usuario)]['partida_terminada'] = True
            with open('buscaminas/data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))
            try:
                keyboard = [[InlineKeyboardButton(t_visible[i][j], callback_data="{} {}".format(i, j))
                             for j in range(len(t_visible[0]))] for i in range(len(t_visible))]
                bot.edit_message_reply_markup(chat_id=id_usuario, message_id=id_mensaje,
                                              reply_markup=InlineKeyboardMarkup(keyboard))
            except BadRequest:
                pass
        else:
            self.enviar_mensaje(bot, id_usuario, "El juego ya terminó. Utiliza /juegos para comenzar uno nuevo.")