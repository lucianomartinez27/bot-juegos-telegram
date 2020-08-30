#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from src.bot_base import BotBase
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.error import BadRequest
from src.tic_tac_toe.funciones import chequear_letra_jugador, obtener_jugada_computadora, tablero_completo, es_ganador

class BotTicTacToe(BotBase):
    def __init__(self):
        super(BotTicTacToe, self).__init__()

    def generar_datos(self, id_usuario):
        # id_usuario se convierte en string porque las claves json deben ser de ese tipo
        self.datos_usuarios[str(id_usuario)] = {}
        self.datos_usuarios[str(id_usuario)]['tablero'] = [" " for i in range(9)]
        self.datos_usuarios[str(id_usuario)]['letra_jugador'] = ''
        self.datos_usuarios[str(id_usuario)]['letra_computadora'] = ''
        self.datos_usuarios[str(id_usuario)]['partida_terminada'] = False
        self.data_manager.save_info(self.datos_usuarios)

    def jugar(self, update, context):
        id_usuario = update.callback_query.message.chat_id
        bot = context.bot
        self.generar_datos(id_usuario)
        custom_keyboard = ['X', 'O']
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=id_usuario,
                         text="Por favor, elige tu lado:",
                         reply_markup=reply_markup)

    def generar_tablero(self, update, context):
        id_usuario = update.message.chat_id
        tablero = self.datos_usuarios[str(id_usuario)]['tablero']
        opciones = [[InlineKeyboardButton(tablero[i], callback_data="{}".format(i))
                     for i in j] for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
        update.message.reply_text('Ta-Te-Ti:', reply_markup=InlineKeyboardMarkup(opciones))

    def responder_mensaje(self, update, context):
        mensaje = update.message.text
        bot = context.bot
        id_usuario = update.message.chat_id
        nombre = update.message.chat.first_name

        if not self.datos_usuarios[str(id_usuario)]['letra_jugador']:
            letra = chequear_letra_jugador(mensaje)
            if letra is not None:
                self.datos_usuarios[str(id_usuario)]['letra_jugador'] = letra[0]
                letra_pc = self.datos_usuarios[str(id_usuario)]['letra_computadora'] = letra[1]
                if letra[0] == "O":
                    tablero = self.datos_usuarios[str(id_usuario)]['tablero']
                    obtener_jugada_computadora(tablero, letra_pc)
                    self.generar_tablero(update, context)
                else:
                    self.generar_tablero(update, context)
            else:
                self.enviar_mensaje(bot, id_usuario, "{}, por favor, ingresa X u O.".format(nombre))
                self.jugar(update, context)

    def responder_boton(self, update, context):
        x = int(update.callback_query.data)
        bot = context.bot
        id_usuario = update.callback_query.message.chat.id
        id_mensaje = update.callback_query.message.message_id
        tablero = self.datos_usuarios[str(id_usuario)]['tablero']
        letra = self.datos_usuarios[str(id_usuario)]['letra_jugador']
        letra_pc = self.datos_usuarios[str(id_usuario)]['letra_computadora']
        partida_terminada = self.datos_usuarios[str(id_usuario)]['partida_terminada']

        if not partida_terminada:
            if tablero_completo(tablero):
                self.enviar_mensaje(bot, id_usuario, "empataste")
                self.datos_usuarios[str(id_usuario)]['partida_terminada'] = True
            tablero[x] = letra
            if es_ganador(tablero, letra):
                self.enviar_mensaje(bot, id_usuario, "ganaste")
                self.datos_usuarios[str(id_usuario)]['partida_terminada'] = True
            elif not tablero_completo(tablero):
                obtener_jugada_computadora(tablero, letra_pc)
                if es_ganador(tablero, letra_pc):
                    self.enviar_mensaje(bot, id_usuario, "perdiste")
                    self.datos_usuarios[str(id_usuario)]['partida_terminada'] = True
            self.data_manager.save_info(self.datos_usuarios)

            try:
                opciones = [[InlineKeyboardButton(tablero[i], callback_data="{}".format(i))
                             for i in j] for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
                bot.edit_message_reply_markup(chat_id=id_usuario, message_id=id_mensaje,
                                              reply_markup=InlineKeyboardMarkup(opciones))
            except BadRequest:
                print("error")
        else:
            self.enviar_mensaje(bot, id_usuario, "El juego ya terminó. Utiliza /juegos para comenzar uno nuevo.")



