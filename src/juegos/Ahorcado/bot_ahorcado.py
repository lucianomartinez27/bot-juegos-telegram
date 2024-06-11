#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from bot_base import BotBase
from .funciones import hangman_template, is_valid_letter
import os


class BotTelegramAhorcado(BotBase):
    def __init__(self):
        self.words = "escopeta mandarina vasija perro zanahoria manzana computadora".upper().split()
        print(os.path.abspath('Ahorcado'))
        super(BotTelegramAhorcado, self).__init__(__file__)

    def name(self):
        return 'Ahorcado'

    def generate_game_state(self, user_id):
        self.users_data[str(user_id)] = {}
        self.users_data[str(user_id)]['word'] = random.choice(self.words)
        self.users_data[str(user_id)]['errors'] = []
        self.users_data[str(user_id)]['guessed'] = []
        self.users_data[str(user_id)]['game_finished'] = False
        self.data_manager.save_info(self.users_data)

    async def play(self, update, context):
        try:
            user_id = update.callback_query.message.chat_id
        except AttributeError:
            user_id = update.message.chat_id

        bot = context.bot
        self.generate_game_state(user_id)
        word = self.users_data[str(user_id)]['word']
        await self.send_message(bot, user_id, "Ingrese una letra como mensaje para jugar:")
        await self.send_message(bot, user_id, hangman_template([], [], word))

    async def answer_message(self, update, context):
        letter = update.message.text.upper()
        bot = context.bot
        user_id = update.message.chat_id
        name = update.message.chat.first_name
        errors = self.users_data[str(user_id)]['errors']
        word = self.users_data[str(user_id)]['word']
        guessed = self.users_data[str(user_id)]['guessed']
        game_finished = self.users_data[str(user_id)]['game_finished']

        if not game_finished:
            if not is_valid_letter(letter):
                await self.send_message(bot, user_id, "POR FAVOR, INGRESA UNA LETRA.")
            elif letter in guessed or letter in errors:
                await self.send_message(bot, user_id, 'YA HAS ELEGIDO ESA LETRA.')
            elif letter in word:
                guessed.append(letter)
            else:
                errors.append(letter)
            await self.send_message(bot, user_id, hangman_template(errors, guessed, word))
            if len(errors) == 6:
                await self.send_message(bot, user_id, "Has perdido\nLa palabra era: {}".format(word))
                self.users_data[str(user_id)]['game_finished'] = True
            elif len(guessed) == len(set(word)):
                await self.send_message(bot, user_id, "Felicitaciones, hasta ganado!.")
                self.users_data[str(user_id)]['game_finished'] = True
            self.data_manager.save_info(self.users_data)
        else:
            await self.game_finished_message(bot, user_id)
