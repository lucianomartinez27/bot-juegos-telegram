#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import os
from telegram_bot import BotTelegram
from utils.data_manager import DataManager
from utils.errors import ModelError


class BotBase(BotTelegram):

    def __init__(self, file):
        self.data_manager = DataManager(os.path.dirname(file))
        self.users_data = self.data_manager.generate_info(dict())
        self.Game = None
        self.initialize_translator()

    def save_all_games(self):
        self.data_manager.save_info({key: value.to_json() for key, value in self.users_data.items()})
    
    def generate_game_state(self, id):
        self.users_data[str(id)] = self.Game()
        self.save_all_games()
        return self.users_data[str(id)]

    def is_inline_game(self):
        return False

    def get_game(self, user_id: int):
        return self.users_data[str(user_id)]

    def do_not_understand_message(self):
        return self._("Sorry, I can't understand you message.")

    async def game_finished_message(self, bot, user_id):
        await self.send_message(bot, user_id, self._("The game ended. Use /games to start a new one"))

    async def answer_message(self, update, context):
        user_id = self.get_user_id(update)
        bot = context.bot
        await self.send_message(bot, user_id, self.do_not_understand_message())

    async def answer_button(self, update, context):
        usuario = self.get_user_id(update)
        bot = context.bot
        await self.send_message(bot, usuario, self.do_not_understand_message())

    async def process_user_action(self, bot, user_id, callback):
        try:
           await callback()
        except ModelError as error:
            await self.send_message(bot, user_id,  self._(error.message))
        except Exception  as error:
            print(error)
            await self.send_message(bot, user_id,  self._("An unexpected error happened"))