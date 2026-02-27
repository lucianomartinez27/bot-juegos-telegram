#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
from base_bot import BotBase
from .hangman import HangManGame 

class BotTelegramAhorcado(BotBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = HangManGame
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }
        self._words_cache = {}

    def game_id(self):
        return '- hangman'

    def name(self):
        return '- Hangman'
    
    async def play(self, update, context):
        user_id = self.get_user_id(update)
        
        # Determine user language from the bot instance
        user_lang = self.language
        
        self.generate_game_state(user_id, user_lang)
        bot = context.bot
        await self.send_message(bot, user_id, self._("Enter a letter as a message to play:"))
        await self.send_message(bot, user_id, self.get_game(user_id).template(self._("word:")))

    def generate_game_state(self, user_id, lang="en"):
        word = self.get_random_word(lang)
        self.users_data[str(user_id)] = self.Game(word)
        self.save_all_games()
        return self.users_data[str(user_id)]

    def get_random_word(self, lang):
        if lang in self._words_cache:
            return random.choice(self._words_cache[lang])

        filename = "words_EN.txt"
        if lang == "es":
            filename = "words_ES.txt"
        
        path = os.path.join(os.path.dirname(__file__), filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                words = [line.strip() for line in f if line.strip()]
            self._words_cache[lang] = words
            return random.choice(words)
        except Exception as e:
            print(f"Error loading words: {e}")
            return "computer" # Fallback

    async def answer_message(self, update, context):
        letter = update.message.text.upper()
        bot = context.bot
        user_id = update.message.chat_id
        game = self.get_game(user_id)

        async def try_letter():
            game.try_letter(letter)
            await self.send_message(bot, user_id, game.template(self._("word:")))
            if game.lost():
                await self.send_message(bot, user_id, self._("You lost\nThe word was: {}").format(game.word()))
        
            if game.won():
                await self.send_message(bot, user_id,  self._("Congratulations, you've won!"))

        if not game.is_finished():
            await self.process_user_action(bot, user_id, try_letter)
            self.save_all_games()
        else:
            await self.game_finished_message(bot, user_id)
