#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from base_bot import BotBase
from .rock_paper_scissor import RockPaperScissorGame, Rock, Scissor, Paper

class BotRockPaperScissorMultiplayer(BotBase):
    def __init__(self):
        super(BotRockPaperScissorMultiplayer, self).__init__(__file__)
        self.users_data = {}
        self.Game = RockPaperScissorGame

    def name(self):
        return 'Piedras Papel y Tijeras Multiplayer'
    
    def is_inline_game(self):
        return True
    
    def generate_inline_markup(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton('Piedra', callback_data='piedra')],
            [InlineKeyboardButton('Papel', callback_data='papel')],
            [InlineKeyboardButton('Tijera', callback_data='tijera')],
        ])
    
    def reset_player_choice(self, context, game, option):
        if game.no_player_choose():
            game.player_one = self.Game.element(option)
            context.user_data['player_symbol'] = option
        elif (game.one_player_choose()):
            game.player_two = self.Game.element(option)
            context.user_data['player_symbol'] = option
        
        
    async def answer_button(self, update, context):        
        user_id = self.get_user_id(update)
        message_id = self.get_message_id(update)
        game = self.users_data.setdefault(self.get_message_id(update), self.generate_game_state(user_id))
        option = update.callback_query.data
        self.reset_player_choice(context, game, option)
        await self.send_message_by_result(game, message_id, context.bot)
        
    
    async def send_message_by_result(self, game, message_id, bot):
        
        if (game.both_players_choose()):
            result = game.play()
            if (result == Rock.name or result == Scissor.name or result == Paper.name):
                start = f"Ganó *{result.upper()}*"
            else:
                start = f"Fue un *EMPATE*"
            message = f"{start}. Uno eligió *{game.player_one_choice().upper()}* y el otro *{game.player_two_choice().upper()}*"
            await bot.edit_message_caption(inline_message_id=message_id, caption= message, reply_markup=self.generate_inline_markup())

