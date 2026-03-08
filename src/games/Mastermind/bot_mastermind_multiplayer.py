#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .bot_mastermind_base import BotMastermindBase
from .multiplayer_mastermind import MultiplayerMasterMind

class BotMastermindMultiplayer(BotMastermindBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = MultiplayerMasterMind
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }

    def game_id(self):
        return '- mastermind_multiplayer'

    def name(self):
        return self._('Mastermind MultiPlayer')

    def is_inline_game(self):
        return True

    def generate_inline_markup(self, game=None):
        if game and not game.combination_set:
            # Standard game keyboard with different callback prefix to avoid conflicts
            return self.create_keyboard("mmm", "c", "delete", "submit")
        # Markup for the creator to set the combination
        return self.create_keyboard("mmm", "set", "del_set", "sub_set")




    async def answer_button(self, update, context):
        query = update.callback_query
        user_id = self.get_user_id(update)
        message_id = self.get_message_id(update)
        user_name = update.effective_user.first_name

        if message_id not in self.users_data:
            self.logger.info(f"User {user_name} ({user_id}) started inline game: {self.name()} ({message_id})")
            game = self.Game(num_digits=4, max_attempts=15)
            game.creator_id = user_id
            game.current_guess = ""
            self.users_data[message_id] = game
            self.save_all_games()
        
        game = self.users_data[message_id]

        if query.data.startswith("mmm_set_"):
            if game.combination_set:
                await query.answer(self._("The combination has already been set."), show_alert=True)
                return
            if game.creator_id != user_id:
                await query.answer(self._("Only the creator can set the combination."), show_alert=True)
                return
            
            color_num = query.data.split("_")[2]
            if color_num in game.current_guess:
                await query.answer(self._("There must be no repeated elements"), show_alert=True)
                return
            
            if len(game.current_guess) < game.num_digits:
                game.current_guess += color_num
                await self.update_setup_message(query, game)
                await query.answer()
            else:
                await query.answer(self._("The combination is invalid. It must have {} elements").format(game.num_digits), show_alert=True)

        elif query.data == "mmm_del_set":
            if game.combination_set: return
            if game.creator_id != user_id:
                await query.answer(self._("Only the creator can set the combination."), show_alert=True)
                return
            if len(game.current_guess) > 0:
                game.current_guess = game.current_guess[:-1]
                await self.update_setup_message(query, game)
                await query.answer()
            else:
                await query.answer("Nothing to delete")

        elif query.data == "mmm_sub_set":
            if game.combination_set: return
            if game.creator_id != user_id:
                await query.answer(self._("Only the creator can set the combination."), show_alert=True)
                return
            if len(game.current_guess) != game.num_digits:
                await query.answer(self._("The combination is invalid. It must have {} elements").format(game.num_digits), show_alert=True)
                return
            
            game.numbers = list(game.current_guess)
            game.combination_set = True
            game.current_guess = "" # Reset for players
            self.save_all_games()
            await query.answer(self._("Combination set! Now others can guess."))
            await self.update_game_message_multiplayer(query, game)

        elif query.data.startswith("mmm_c_"):
            if not game.combination_set:
                await query.answer(self._("Wait for the creator to set the combination."), show_alert=True)
                return
            if game.finished():
                await query.answer(self._("The game has already finished."), show_alert=True)
                return
            if user_id == game.creator_id:
                 await query.answer(self._("The creator cannot play!"), show_alert=True)
                 return

            color_num = query.data.split("_")[2]
            if color_num in game.current_guess:
                await query.answer(self._("There must be no repeated elements"), show_alert=True)
                return
            
            if len(game.current_guess) < game.num_digits:
                game.current_guess += color_num
                await self.update_game_message_multiplayer(query, game)
                await query.answer()
            else:
                await query.answer(self._("The combination is invalid. It must have {} elements").format(game.num_digits), show_alert=True)

        elif query.data == "mmm_delete":
            if not game.combination_set or game.finished(): return
            if len(game.current_guess) > 0:
                game.current_guess = game.current_guess[:-1]
                await self.update_game_message_multiplayer(query, game)
                await query.answer()
            else:
                await query.answer("Nothing to delete")

        elif query.data == "mmm_submit":
            if not game.combination_set: return
            if game.finished():
                await query.answer(self._("The game has already finished."), show_alert=True)
                return
            if len(game.current_guess) != game.num_digits:
                await query.answer(self._("The combination is invalid. It must have {} elements").format(game.num_digits), show_alert=True)
                return
            
            attempt = game.current_guess
            game.current_guess = ""
            await self.make_attempt_multiplayer(context.bot, message_id, attempt, user_name, query)

    async def update_setup_message(self, query, game):
        current_colors = self.format_attempt(game.current_guess)
        text = self._("MASTERMIND MULTIPLAYER\n\nSetting up the game.\nCreator: Select the secret combination.")
        text += f"\n\n" + self._("Current selection: {}").format(current_colors)
        await query.edit_message_text(text, reply_markup=self.generate_inline_markup(game))

    async def update_game_message_multiplayer(self, query, game):
        current_colors = self.format_attempt(game.current_guess)
        text = game.template(
            self._("You have {} attempts left "), 
            self._("DEADS - INJURED"),
            formatter=self.format_attempt
        )
        text += f"\n\n" + self._("Current selection: {}").format(current_colors)
        await query.edit_message_text(text, reply_markup=self.generate_inline_markup(game))

    async def make_attempt_multiplayer(self, bot, message_id, attempt, name, query):
        await self.make_attempt_logic(bot, message_id, attempt, name, query, game=self.users_data[message_id])
