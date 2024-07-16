#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from base_bot import BotBase
from .rock_paper_scissor import RockPaperScissorGame, Rock, Scissor, Paper

class BotRockPaperScissor(BotBase):
    def __init__(self):
        super(BotRockPaperScissor, self).__init__(__file__)
        self.users_data = { key: RockPaperScissorGame.from_json(value) for key, value in self.users_data.items() }
        self.Game = RockPaperScissorGame

    def name(self):
        return '- Piedras Papel y Tijeras'
    
    async def play(self, update, context):
        await update.callback_query.message.reply_text(self.name(), reply_markup=InlineKeyboardMarkup(self.element_options()))
    
    def element_options(self):
        return [
            [InlineKeyboardButton('Piedra', callback_data='piedra')],
            [InlineKeyboardButton('Papel', callback_data='papel')],
            [InlineKeyboardButton('Tijera', callback_data='tijera')],
        ]

    async def answer_button(self, update, context):
        option = update.callback_query.data
        bot = context.bot
        user_id = self.get_user_id(update)
        game = self.Game(self.Game.element(option), self.Game.random_choice())
        message = self.get_message_by_result(game)
        await self.send_message(bot, user_id, message, parse_mode='markdown')
    
    def get_message_by_result(self, game):
        result = game.play()
        if (result == Rock.name or result == Scissor.name or result == Paper.name):
            winner = f"Ganó *{result.upper()}*"
        else:
            winner = f"Fue un *{result.upper()}*"
        return f"{winner}. Tu elegiste *{game.player_one_choice().upper()}* la computadora eligió *{game.player_two_choice().upper()}*"

