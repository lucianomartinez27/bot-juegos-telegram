#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Juego : MUERTOS Y HERIDOS - MASTERMIND
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .bot_mastermind_base import BotMastermindBase
from games.Mastermind.mastermind import MasterMind


class BotMastermind(BotMastermindBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = MasterMind
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }

    def format_attempt(self, attempt):
        return "".join([self.num_to_color.get(num, num) for num in attempt])

    def game_id(self):
        return '- mastermind'

    def name(self):
        return '- Mastermind'

    async def play(self, update, context):
        difficulties = [
            [InlineKeyboardButton(self._("Easy"), callback_data="mm_diff_easy")],
            [InlineKeyboardButton(self._("Medium"), callback_data="mm_diff_medium")],
            [InlineKeyboardButton(self._("Hard"), callback_data="mm_diff_hard")]
        ]
        
        await update.callback_query.message.reply_text(
            self._("Select difficulty level:"), 
            reply_markup=InlineKeyboardMarkup(difficulties)
        )

    async def start_game(self, update, context, difficulty):
        user_id = self.get_user_id(update)
        user_name = update.effective_user.first_name
        bot = context.bot
        settings = self.difficulty_settings[difficulty]
        self.logger.info(f"User {user_name} ({user_id}) started game: {self.name()} ({difficulty})")
        game = self.generate_game_state(user_id, settings["num_digits"], settings["max_attempts"])
        
        await self.send_message(bot, user_id,  self._('MASTERMIND'))
        color_list = " ".join(self.colors)
        instructions = self._("Guess a {}-color combination (no repeats) using these colors: \n{}").format(game.num_digits, color_list) + "\n\n" + \
                       self._("Results meaning:\n⚫: Correct color and position\n⚪: Correct color but wrong position\n❌: No matches")
        await self.send_message(bot, user_id, instructions)
        
        status_msg = self._("To win, you need to get {} ⚫. You will have {} attempts.").format(game.num_digits, game.max_attempts)
        await self.send_message(bot, user_id, status_msg, reply_markup=self.generate_inline_markup(game))

    def generate_game_state(self, user_id, num_digits=4, max_attempts=15):
        self.users_data[str(user_id)] = self.Game(num_digits, max_attempts)
        self.users_data[str(user_id)].current_guess = ""
        self.save_all_games()
        return self.users_data[str(user_id)]

    def generate_inline_markup(self, game=None):
        return self.generate_inline_markup_base()

    async def answer_button(self, update, context):
        query = update.callback_query
        user_id = self.get_user_id(update)
        game = self.get_game(user_id)
        bot = context.bot

        if query.data.startswith("mm_diff_"):
            difficulty = query.data.split("_")[2]
            await query.answer()
            await query.edit_message_text(self._("Difficulty set to {}").format(self._(difficulty.capitalize())))
            await self.start_game(update, context, difficulty)
            return

        if game.finished():
            await query.answer(self._("The game ended. Use /games to start a new one"), show_alert=True)
            return

        if query.data.startswith("mm_c_"):
            color_num = query.data.split("_")[2]
            if not hasattr(game, 'current_guess'):
                game.current_guess = ""
            
            if color_num in game.current_guess:
                await query.answer(self._("There must be no repeated elements"), show_alert=True)
                return
                
            if len(game.current_guess) < game.num_digits:
                game.current_guess += color_num
                current_colors = self.format_attempt(game.current_guess)
                await query.answer(f"Selected: {current_colors}")
                await self.update_game_message(query, game)
            else:
                await query.answer(self._("The combination is invalid. It must have {} elements").format(game.num_digits), show_alert=True)

        elif query.data == "mm_delete":
            if hasattr(game, 'current_guess') and len(game.current_guess) > 0:
                game.current_guess = game.current_guess[:-1]
                await query.answer("Deleted")
                await self.update_game_message(query, game)
            else:
                await query.answer("Nothing to delete")

        elif query.data == "mm_submit":
            if not hasattr(game, 'current_guess') or len(game.current_guess) != game.num_digits:
                await query.answer(self._("The combination is invalid. It must have {} elements").format(game.num_digits), show_alert=True)
                return
            
            attempt = game.current_guess
            game.current_guess = "" # Reset for next attempt
            name = update.effective_user.first_name if update.effective_user else "Player"
            await self.make_attempt(bot, user_id, attempt, name, query)

    async def update_game_message(self, query, game):
        current_colors = self.format_attempt(getattr(game, 'current_guess', ""))
        text = game.template(
            self._("You have {} attempts left "), 
            self._("Results"),
            formatter=self.format_attempt
        )
        text += f"\n\n" + self._("Current selection: {}").format(current_colors)
        await query.edit_message_text(text, reply_markup=self.generate_inline_markup(game))

    async def make_attempt(self, bot, user_id, attempt, name="Player", query=None):
        async def do_attempt():
            await self.make_attempt_logic(bot, user_id, attempt, name, query)

        await self.process_user_action(bot, user_id, do_attempt)
                
                
