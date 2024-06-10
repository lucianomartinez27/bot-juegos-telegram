#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bot_base import BotBase
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.error import BadRequest
from juegos.TaTeTi.funciones import chequear_letra_jugador, obtener_jugada_computadora, tablero_completo, es_ganador


class BotTicTacToe(BotBase):
    def __init__(self):
        super(BotTicTacToe, self).__init__(__file__)

    def name(self):
        return 'TaTeTi'

    def generate_game_state(self, user_id):
        # user_id se convierte en string porque las claves json deben ser de ese tipo
        self.users_data[str(user_id)] = {}
        self.users_data[str(user_id)]['board'] = [" " for i in range(9)]
        self.users_data[str(user_id)]['player_symbol'] = ''
        self.users_data[str(user_id)]['letra_computadora'] = ''
        self.users_data[str(user_id)]['game_finished'] = False
        self.data_manager.save_info(self.users_data)

    async def play(self, update, context):

        user_id = self.get_user_id(update)
        bot = context.bot
        self.generate_game_state(user_id)
        custom_keyboard = [['X', 'O']]
        reply_markup = ReplyKeyboardMarkup(custom_keyboard)
        await bot.send_message(chat_id=user_id,
                         text="Por favor, elige tu lado:",
                         reply_markup=reply_markup)


    def generate_markup(self, update, context):
        user_id = self.get_user_id(update)
        board = self.users_data[str(user_id)]['board']
        opciones = [[InlineKeyboardButton(board[i], callback_data="{}".format(i))
                     for i in j] for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
        return InlineKeyboardMarkup(opciones)

    async def generar_tablero(self, update, context):
        await update.message.reply_text('Ta-Te-Ti:', reply_markup=self.generate_markup(update, context))

    async def answer_message(self, update, context):
        mensaje = update.message.text
        bot = context.bot
        user_id = self.get_user_id(update)
        name = update.message.chat.first_name

        if not self.users_data[str(user_id)]['player_symbol']:
            letra = chequear_letra_jugador(mensaje)
            if letra is not None:
                self.users_data[str(user_id)]['player_symbol'] = letra[0]
                letra_pc = self.users_data[str(user_id)]['letra_computadora'] = letra[1]
                if letra[0] == "O":
                    board = self.users_data[str(user_id)]['board']
                    obtener_jugada_computadora(board, letra_pc)
                    await self.generar_tablero(update, context)
                else:
                    await self.generar_tablero(update, context)
            else:
                await self.send_message(bot, user_id, "{}, por favor, ingresa X u O.".format(name))
                await self.play(update, context)

    async def update_board(self, bot, board, chat_id=None, message_id=None, id_mensaje_inline=None):
        opciones = [[InlineKeyboardButton(board[i], callback_data="{}".format(i))
                        for i in j] for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        inline_message_id=id_mensaje_inline,
                                        reply_markup=InlineKeyboardMarkup(opciones))


    async def answer_button(self, update, context):
        casilla = int(update.callback_query.data)
        bot = context.bot
        user_id = self.get_user_id(update)
        message_id = self.get_message_id(update)
        board = self.users_data[str(user_id)]['board']
        letra = self.users_data[str(user_id)]['player_symbol']
        letra_pc = self.users_data[str(user_id)]['letra_computadora']
        game_finished = self.users_data[str(user_id)]['game_finished']

        if not game_finished:
            if tablero_completo(board):
                await self.send_message(bot, user_id, "empataste")
                self.users_data[str(user_id)]['game_finished'] = True
            board[casilla] = letra
            if es_ganador(board, letra):
                await self.send_message(bot, user_id, "ganaste")
                self.users_data[str(user_id)]['game_finished'] = True
            elif not tablero_completo(board):
                obtener_jugada_computadora(board, letra_pc)
                if es_ganador(board, letra_pc):
                    await self.send_message(bot, user_id, "perdiste")
                    self.users_data[str(user_id)]['game_finished'] = True
            self.data_manager.save_info(self.users_data)
            await self.update_board(bot, board, user_id, message_id)
        else:
            await self.send_message(bot, user_id, "El juego ya terminó. Utiliza /juegos para comenzar uno nuevo.")
