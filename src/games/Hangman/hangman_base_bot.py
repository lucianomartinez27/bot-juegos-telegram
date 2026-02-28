#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import string
from abc import abstractmethod
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from base_bot import BotBase
from utils.errors import ModelError


class BotHangmanBase(BotBase):
    def __init__(self, file=__file__):
        super().__init__(file)
        self._words_cache = {}

    @abstractmethod
    def game_id(self):
        pass

    @abstractmethod
    def name(self):
        pass

    def generate_inline_markup(self, game=None):
        keyboard = []
        row = []
        spanish_upper = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        letters = self.language == "es" and spanish_upper or string.ascii_uppercase
        for i, letter in enumerate(letters):
            text = letter
            if game and game.letter_has_been_tried(letter):
                text = "-"
            
            row.append(InlineKeyboardButton(text, callback_data=f"h_{letter}"))
            if (i + 1) % 7 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        return InlineKeyboardMarkup(keyboard)

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
                words = [line.strip().upper() for line in f if line.strip()]
            self._words_cache[lang] = words
            return random.choice(words)
        except Exception as e:
            print(f"Error loading words: {e}")
            return "COMPUTER" # Fallback

    async def answer_button(self, update, context):
        user_id = self.get_user_id(update)
        message_id = self.get_message_id(update)
        query = update.callback_query

        if message_id not in self.users_data:
            # For inline games, we often use message_id as key
            self.users_data[message_id] = self.generate_game_state(user_id, self.language)

        game = self.users_data[message_id]

        if game.is_finished():
            await query.answer(self._("The game has already finished."))
            return

        data = query.data
        if not data.startswith("h_"):
            return

        letter = data.split("_")[1]

        try:
            can_play = await self.assign_user_turn(game, query, user_id)
            if not can_play:
                return

            game.try_letter(letter)

            caption = game.template(self._("word:"))
            if game.won():
                caption += "\n\n" + self._("Congratulations, you've won!")
            elif game.lost():
                caption += "\n\n" + self._("You lost\nThe word was: {}").format(game.word())

            await self.send_keyboard(caption, update, context, game, message_id)
            self.save_all_games()
            await query.answer()
        except ModelError as e:
            await query.answer(self._(e.message), show_alert=True)
        except Exception as e:
            print(f"Error in hangman multiplayer: {e}")
            await query.answer(self._("An unexpected error happened"), show_alert=True)


    async def send_keyboard(self, caption, update, context, game, message_id):
        raise NotImplementedError

    async def assign_user_turn(self, game, query, user_id):
        if game.last_player_id == user_id:
            await query.answer(self._("It is not your turn! Wait for another player."), show_alert=True)
            return False
        else:
            game.last_player_id = user_id
            return True

