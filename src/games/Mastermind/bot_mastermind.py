#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Juego : MUERTOS Y HERIDOS - MASTERMIND
"""

from base_bot import BotBase
from games.Mastermind.mastermind import MasterMind


class BotMastermind(BotBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = MasterMind
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }

    def name(self):
        return '- Mastermind'

    async def play(self, update, context):
        user_id = update.callback_query.message.chat_id
        bot = context.bot
        self.generate_game_state(user_id)
        await self.send_message(bot, user_id,  self._('MASTERMIND'))
        await self.send_message(bot, user_id,
                             self._("Guess a 4-digit number (no repeats). If you guess the number but not the position ") + \
                             self._("you have one injured. If you guess the number and its position, you have one dead"))
        await self.send_message(bot, user_id,  self._("To win, you need to get 4 dead. You will have 15 attempts."))

    async def answer_message(self, update, context):
        attempt = update.message.text
        bot = context.bot
        user_id = update.message.chat_id
        name = update.message.chat.first_name
        game = self.get_game(user_id)

        async def make_attempt():
            game.check_number(attempt)
            await self.send_message(bot, user_id, game.template())
            self.save_all_games()
            
            if game.is_winner():
                await self.send_message(bot, user_id,  self._("Congratulations, {}, YOU WON!!\n")\
                                    .format(name))
            elif game.is_looser():
                await self.send_message(bot, user_id,  self._("I'm sorry, {}, YOU LOST!!\n The number was {}").format(name, "".join(game.numbers)))

        if game.finished():
            await self.game_finished_message(bot, user_id)

        else:
            await self.process_user_action(bot, user_id, make_attempt)
                
                
