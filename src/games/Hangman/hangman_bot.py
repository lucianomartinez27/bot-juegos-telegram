#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .hangman_base_bot import BotHangmanBase
from .hangman import HangManGame 

class BotTelegramAhorcado(BotHangmanBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = HangManGame
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }

    def game_id(self):
        return '- hangman'

    def name(self):
        return '- Hangman'
    

    async def play(self, update, context):
        user_id = self.get_user_id(update)
        
        # Determine user language from the bot instance
        user_lang = self.language
        
        game = self.generate_game_state(user_id, user_lang)
        bot = context.bot
        await self.send_message(bot, user_id, self._("Select a letter to play:"), reply_markup=self.generate_inline_markup(game), parse_mode='HTML')

    async def assign_user_turn(self, game, query, user_id):
        return True

    async def send_keyboard(self, caption, update, context, game, message_id):
        user_id = self.get_user_id(update)
        await context.bot.edit_message_text(
            message_id=message_id,
            chat_id=user_id,
            text=f"<pre>\n{caption}\n</pre>",
            reply_markup=self.generate_inline_markup(game),
            parse_mode='HTML'
        )