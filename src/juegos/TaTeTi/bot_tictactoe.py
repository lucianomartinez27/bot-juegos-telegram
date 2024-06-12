#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bot_base import BotBase
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from .tictactoe import AgainstComputerTicTacToe

class BotTicTacToe(BotBase):
    def __init__(self):
        super(BotTicTacToe, self).__init__(__file__)
        self.Game = AgainstComputerTicTacToe
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }
    
    def name(self):
        return 'TaTeTi'

    async def play(self, update, context):

        user_id = self.get_user_id(update)
        bot = context.bot
        self.generate_game_state(user_id)
        custom_keyboard = [['X', 'O']]
        await bot.send_message(chat_id=user_id,
                         text="Por favor, elige tu lado:",
                         reply_markup=ReplyKeyboardMarkup(custom_keyboard))


    def generate_markup(self, update, context):
        user_id = self.get_user_id(update)
        board_buttons = [[InlineKeyboardButton(self.get_game(user_id).board[i], callback_data="{}".format(i))
                     for i in j] for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
        return InlineKeyboardMarkup(board_buttons)

    async def generate_board(self, update, context):
        await update.message.reply_text('Ta-Te-Ti:', reply_markup=self.generate_markup(update, context))

    async def answer_message(self, update, context):
        message = update.message.text
        user_id = self.get_user_id(update)
        game = self.get_game(user_id)
        if not game.started():
            game.get_players_symbols(message)
            if game.computer_plays_first():
                game.make_computer_movement()    
            await self.generate_board(update, context)

    async def update_board(self, bot, board, chat_id=None, message_id=None, id_mensaje_inline=None):
        opciones = [[InlineKeyboardButton(board[i], callback_data="{}".format(i))
                        for i in j] for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
        await bot.edit_message_reply_markup(chat_id=chat_id,
                                        message_id=message_id,
                                        inline_message_id=id_mensaje_inline,
                                        reply_markup=InlineKeyboardMarkup(opciones))


    async def answer_button(self, update, context):
        cell = int(update.callback_query.data)
        bot = context.bot
        user_id = self.get_user_id(update)
        message_id = self.get_message_id(update)
        game = self.get_game(user_id)

        if game.finished():
            await self.game_finished_message(bot, user_id)
        else:
            game.mark_cell(game.player_symbol, cell)            
            if not game.finished():
                game.make_computer_movement()

            if game.finished():
                if game.is_winner(game.player_symbol):
                    await self.send_message(bot, user_id, 'Ganaste')
                elif game.is_winner(game.computer_symbol):
                    await self.send_message(bot, user_id, 'Perdiste')
                else: #isTie
                    await self.send_message(bot, user_id, 'Empataste')
            self.save_all_games()
            await self.update_board(bot, game.board, user_id, message_id)
            
        
           