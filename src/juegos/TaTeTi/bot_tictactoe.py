#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bot_base import BotBase
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.error import BadRequest
from juegos.TaTeTi.funciones import chequear_letra_jugador, obtener_jugada_computadora, tablero_completo, es_ganador
import os


class BotTicTacToe(BotBase):
    def __init__(self):
        super(BotTicTacToe, self).__init__(__file__)

    def nombre(self):
        return 'TaTeTi'

    def generar_datos(self, id_usuario):
        # id_usuario se convierte en string porque las claves json deben ser de ese tipo
        self.datos_usuarios[str(id_usuario)] = {}
        self.datos_usuarios[str(id_usuario)]['tablero'] = [" " for i in range(9)]
        self.datos_usuarios[str(id_usuario)]['letra_jugador'] = ''
        self.datos_usuarios[str(id_usuario)]['letra_computadora'] = ''
        self.datos_usuarios[str(id_usuario)]['partida_terminada'] = False
        self.data_manager.save_info(self.datos_usuarios)

    async def jugar(self, update, context):

        id_usuario = self.generar_id_usuario(update)
        bot = context.bot
        self.generar_datos(id_usuario)
        custom_keyboard = [['X', 'O']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        await bot.send_message(chat_id=id_usuario,
                         text="Por favor, elige tu lado:",
                         reply_markup=reply_markup)


    def generar_markup(self, update, context):
        id_usuario = self.generar_id_usuario(update)
        tablero = self.datos_usuarios[str(id_usuario)]['tablero']
        opciones = [[InlineKeyboardButton(tablero[i], callback_data="{}".format(i))
                     for i in j] for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
        return InlineKeyboardMarkup(opciones)

    async def generar_tablero(self, update, context):
        await update.message.reply_text('Ta-Te-Ti:', reply_markup=self.generar_markup(update, context))

    async def responder_mensaje(self, update, context):
        mensaje = update.message.text
        bot = context.bot
        id_usuario = self.generar_id_usuario(update)
        nombre = update.message.chat.first_name

        if not self.datos_usuarios[str(id_usuario)]['letra_jugador']:
            letra = chequear_letra_jugador(mensaje)
            if letra is not None:
                self.datos_usuarios[str(id_usuario)]['letra_jugador'] = letra[0]
                letra_pc = self.datos_usuarios[str(id_usuario)]['letra_computadora'] = letra[1]
                if letra[0] == "O":
                    tablero = self.datos_usuarios[str(id_usuario)]['tablero']
                    obtener_jugada_computadora(tablero, letra_pc)
                    await self.generar_tablero(update, context)
                else:
                    await self.generar_tablero(update, context)
            else:
                await self.enviar_mensaje(bot, id_usuario, "{}, por favor, ingresa X u O.".format(nombre))
                await self.jugar(update, context)

    async def actualizar_tablero(self, bot, tablero, chat_id=None, id_mensaje=None, id_mensaje_inline=None):
        try:
            opciones = [[InlineKeyboardButton(tablero[i], callback_data="{}".format(i))
                         for i in j] for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
            await bot.edit_message_reply_markup(chat_id=chat_id,
                                          message_id=id_mensaje,
                                          inline_message_id=id_mensaje_inline,
                                          reply_markup=InlineKeyboardMarkup(opciones))
        except BadRequest as error:
            print(error)

    async def responder_boton(self, update, context):
        casilla = int(update.callback_query.data)
        bot = context.bot
        id_usuario = self.generar_id_usuario(update)
        id_mensaje = self.generar_id_mensaje(update)
        tablero = self.datos_usuarios[str(id_usuario)]['tablero']
        letra = self.datos_usuarios[str(id_usuario)]['letra_jugador']
        letra_pc = self.datos_usuarios[str(id_usuario)]['letra_computadora']
        partida_terminada = self.datos_usuarios[str(id_usuario)]['partida_terminada']

        if not partida_terminada:
            if tablero_completo(tablero):
                await self.enviar_mensaje(bot, id_usuario, "empataste")
                self.datos_usuarios[str(id_usuario)]['partida_terminada'] = True
            tablero[casilla] = letra
            if es_ganador(tablero, letra):
                await self.enviar_mensaje(bot, id_usuario, "ganaste")
                self.datos_usuarios[str(id_usuario)]['partida_terminada'] = True
            elif not tablero_completo(tablero):
                obtener_jugada_computadora(tablero, letra_pc)
                if es_ganador(tablero, letra_pc):
                    await self.enviar_mensaje(bot, id_usuario, "perdiste")
                    self.datos_usuarios[str(id_usuario)]['partida_terminada'] = True
            self.data_manager.save_info(self.datos_usuarios)
            await self.actualizar_tablero(bot, tablero, id_usuario, id_mensaje)
        else:
            await self.enviar_mensaje(bot, id_usuario, "El juego ya terminó. Utiliza /juegos para comenzar uno nuevo.")
