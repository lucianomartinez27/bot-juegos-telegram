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
    
    async def reset_player_choice(self, context, update, game, option):
        message_id = self.get_message_id(update)
        user_full_name = update.effective_user.full_name
        users = context.bot_data.setdefault(message_id, {'first_player_name': '', 'second_player_name': ''})
        if game.no_player_choose():
            users['first_player_name'] = user_full_name
            game.player_one = self.Game.element(option)
            context.user_data[message_id] = option
            message = f"*{user_full_name}* ya eligió su opción."
            await context.bot.edit_message_caption(inline_message_id=message_id, caption= message, reply_markup=self.generate_inline_markup(), parse_mode='markdown')
        elif game.one_player_choose() and not context.user_data.get(message_id):
            users['second_player_name'] = user_full_name
            game.player_two = self.Game.element(option)
        
        
    async def answer_button(self, update, context):        
        user_id = self.get_user_id(update)
        message_id = self.get_message_id(update)
        game = self.users_data.setdefault(message_id, self.generate_game_state(user_id))
        option = update.callback_query.data
        await self.reset_player_choice(context, update, game, option)
        if (game.both_players_choose()):
            await self.send_message_by_result(game, message_id, context)
  
        
    
    async def send_message_by_result(self, game, message_id, context):
        
        if (game.both_players_choose()):
            result = game.play()
            if (result == Rock.name or result == Scissor.name or result == Paper.name):
                start = f"Ganó *{result.upper()}*"
            else:
                start = f"Fue un *EMPATE*"
            first_player_name =  context.bot_data[message_id]['first_player_name']
            second_player_name = context.bot_data[message_id]['second_player_name']
            message = f"{start}. *{first_player_name}* eligió *{game.player_one_choice().upper()}* y *{second_player_name}* eligió *{game.player_two_choice().upper()}*"
            await context.bot.edit_message_caption(inline_message_id=message_id, caption= message, reply_markup=self.generate_inline_markup(), parse_mode='markdown')

