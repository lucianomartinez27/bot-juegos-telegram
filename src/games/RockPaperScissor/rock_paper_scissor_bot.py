#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from base_bot import BotBase
from .rock_paper_scissor import RockPaperScissorGame, Rock, Scissor, Paper

class BotRockPaperScissor(BotBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = RockPaperScissorGame
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }

    def game_id(self):
        return '- rock_paper_scissor'

    def name(self):
        return  self._('- Rock, Paper, Scissors')
    
    async def play(self, update, context):
        await update.callback_query.message.reply_text(self.name(), reply_markup=InlineKeyboardMarkup(self.element_options()))
    
    def element_options(self):
        return [
            [InlineKeyboardButton(self._('Rock'), callback_data='rock')],
            [InlineKeyboardButton(self._('Paper'), callback_data='paper')],
            [InlineKeyboardButton(self._('Scissors'), callback_data='scissors')],
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
        if result == Rock.name or result == Scissor.name or result == Paper.name:
            if game.last_winner_is_player_one():
                start = self._("*You won*")
            else:
                start = self._("*You lost*")
        else:
            start = self._(f"It was a *TIE*")
        return self._("{}. You chose *{}*, the computer chose *{}*").format(
            start, self._(game.player_one_choice().upper()), self._(game.player_two_choice().upper()))

