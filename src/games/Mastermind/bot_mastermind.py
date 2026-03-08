#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Juego : MUERTOS Y HERIDOS - MASTERMIND
"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from base_bot import BotBase
from games.Mastermind.mastermind import MasterMind


class BotMastermind(BotBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = MasterMind
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }
        self.difficulty_settings = {
            "easy": {"num_digits": 3, "max_attempts": 15},
            "medium": {"num_digits": 4, "max_attempts": 15},
            "hard": {"num_digits": 5, "max_attempts": 12}
        }
        self.colors = ["🔴", "🔵", "🟢", "🟡", "🟣", "🟠", "🟤", "⚪"]
        self.color_to_num = {color: str(i) for i, color in enumerate(self.colors)}
        self.num_to_color = {str(i): color for i, color in enumerate(self.colors)}

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
        await self.send_message(bot, user_id,
                             self._("Guess a {}-color combination (no repeats) using these colors: \n{}").format(game.num_digits, color_list) + "\n\n" + \
                             self._("If you guess the color but not the position, you have one injured. If you guess the color and its position, you have one dead"))
        await self.send_message(bot, user_id,  self._("To win, you need to get {} dead. You will have {} attempts.")\
                                .format(game.num_digits, game.max_attempts))

    def generate_game_state(self, user_id, num_digits=4, max_attempts=15):
        self.users_data[str(user_id)] = self.Game(num_digits, max_attempts)
        self.save_all_games()
        return self.users_data[str(user_id)]

    async def answer_button(self, update, context):
        query = update.callback_query
        if query.data.startswith("mm_diff_"):
            difficulty = query.data.split("_")[2]
            await query.answer()
            await query.edit_message_text(self._("Difficulty set to {}").format(self._(difficulty.capitalize())))
            await self.start_game(update, context, difficulty)

    async def answer_message(self, update, context):
        text = update.message.text
        bot = context.bot
        user_id = update.message.chat_id
        name = update.message.chat.first_name
        game = self.get_game(user_id)

        # Convert emojis to numbers
        attempt = ""
        i = 0
        while i < len(text):
            found = False
            for color, num in self.color_to_num.items():
                if text[i:i+len(color)] == color:
                    attempt += num
                    i += len(color)
                    found = True
                    break
            if not found:
                attempt += text[i]
                i += 1

        async def make_attempt():
            game.check_number(attempt)
            await self.send_message(bot, user_id, game.template(
                self._("You have {} attempts left "), 
                self._("DEADS - INJURED"),
                formatter=self.format_attempt
            ))
            self.save_all_games()
            
            if game.is_winner():
                await self.send_message(bot, user_id,  self._("Congratulations, {}, YOU WON!!\n")\
                                    .format(name))
            elif game.is_looser():
                solution = self.format_attempt("".join(game.numbers))
                await self.send_message(bot, user_id,  self._("I'm sorry, {}, YOU LOST!!\n The combination was {}").format(name, solution))

        if game.finished():
            await self.game_finished_message(update, context)

        else:
            await self.process_user_action(bot, user_id, make_attempt)
                
                
