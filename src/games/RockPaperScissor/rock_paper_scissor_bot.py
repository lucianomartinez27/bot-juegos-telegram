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
            [InlineKeyboardButton('Piedra', callback_data='rock')],
            [InlineKeyboardButton('Papel', callback_data='paper')],
            [InlineKeyboardButton('Tijera', callback_data='scissor')],
        ]

    async def answer_button(self, update, context):
        option = update.callback_query.data
        bot = context.bot
        user_id = self.get_user_id(update)
        game = self.Game(self.Game.element(option), self.Game.random_choice())
        message = self.get_message_by_result(game.play())
        await self.send_message(bot, user_id, message)
    
    def get_message_by_result(self, winner):
        if (winner == Rock.name):
            return 'Ganó Piedra'
        if (winner == Scissor.name):
            return 'Ganó Tijera'
        if (winner == Paper.name):
            return 'Ganó Papel'
        return 'Fue un emptate'
