#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bot_base import BotBase
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from .funciones import crear_tablero, despejar_tablero, tablero_visible_inicial, verificar_tablero, descubrir_tablero



class BotBuscaminas(BotBase):
    def __init__(self):
        super(BotBuscaminas, self).__init__(__file__)

    def name(self):
        return 'Buscaminas'

    def generate_game_state(self, user_id):
        # user_id se convierte en string porque las claves json deben ser de ese tipo
        self.users_data[str(user_id)] = {}
        bombas = self.users_data[str(user_id)]['bombas'] = 10
        t_oculto = self.users_data[str(user_id)]['tablero_oculto'] = crear_tablero(8, 8, bombas)
        self.users_data[str(user_id)]['tablero_visible'] = tablero_visible_inicial(t_oculto)
        self.users_data[str(user_id)]['game_finished'] = False
        self.data_manager.save_info(self.users_data)

    async def play(self, update, context):
        user_id = update.callback_query.message.chat_id
        self.generate_game_state(user_id)
        board = self.users_data[str(user_id)]['tablero_visible']

        opciones = [[InlineKeyboardButton(board[i][j], callback_data="{} {}".format(i, j))
                     for j in range(len(board[0]))] for i in range(len(board))]

        await update.callback_query.message.reply_text('Buscaminas:', reply_markup=InlineKeyboardMarkup(opciones))

    async def answer_button(self, update, context):
        x, y = update.callback_query.data.split()
        bot = context.bot
        user_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id
        t_oculto = self.users_data[str(user_id)]['tablero_oculto']
        t_visible = self.users_data[str(user_id)]['tablero_visible']
        bombas = self.users_data[str(user_id)]['bombas']
        game_finished = self.users_data[str(user_id)]['game_finished']
        if not game_finished:
            despejar_tablero(int(x), int(y), t_oculto, t_visible)
            if t_oculto[int(x)][int(y)] == 9:
                await self.send_message(bot, user_id, "Perdiste")
                descubrir_tablero(t_visible, t_oculto)
                self.users_data[str(user_id)]['game_finished'] = True
            if verificar_tablero(t_visible, bombas):
                descubrir_tablero(t_visible, t_oculto)
                await self.send_message(bot, user_id, "Ganaste")
                self.users_data[str(user_id)]['game_finished'] = True
            self.data_manager.save_info(self.users_data)
            try:
                keyboard = [[InlineKeyboardButton(t_visible[i][j], callback_data="{} {}".format(i, j))
                             for j in range(len(t_visible[0]))] for i in range(len(t_visible))]
                await bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id,
                                              reply_markup=InlineKeyboardMarkup(keyboard))
            except BadRequest:
                pass
        else:
            await self.game_finished_message(bot, user_id)