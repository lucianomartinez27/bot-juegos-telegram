#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Juego : MUERTOS Y HERIDOS - MASTERMIND
"""

from bot_base import BotBase
from juegos.Mastermind.mastermind import MasterMind


class BotMastermind(BotBase):
    def __init__(self):
        super(BotMastermind, self).__init__(__file__)
        self.users_data = { key: MasterMind.from_json(value) for key, value in self.users_data.items() }
        self.Game = MasterMind

    def name(self):
        return 'Mastermind'

    async def play(self, update, context):
        user_id = update.callback_query.message.chat_id
        bot = context.bot
        self.generate_game_state(user_id)
        await self.send_message(bot, user_id, 'MUERTOS Y HERIDOS (MASTERMIND)')
        await self.send_message(bot, user_id,
                            'Adivina un número de 4 dígitos (ninguno repetido), si aciertas el número, pero no la posición '
                            'tienes un herido. Si aciertas el número y su posición tienes un muerto.')
        await self.send_message(bot, user_id, 'Para ganar necesitas conseguir 4 muertos. Tendrás 15 intentos.')

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
                await self.send_message(bot, user_id, "Felicidades, {}, GANASTE!!\n "\
                                    .format(name))
            elif game.is_looser():
                await self.send_message(bot, user_id, "Lo siento, {}, PERDISTE!!\n El número era {}".format(name, "".join(game.numbers)))

        if game.finished():
            await self.game_finished_message(bot, user_id)

        else:
            await self.process_user_action(bot, user_id, make_attempt)
                
                
