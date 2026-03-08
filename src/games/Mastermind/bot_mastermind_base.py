#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from base_bot import BotBase
from utils.errors import ModelError

class BotMastermindBase(BotBase):
    def __init__(self, file):
        super().__init__(file)
        self.difficulty_settings = {
            "easy": {"num_digits": 3, "max_attempts": 15},
            "medium": {"num_digits": 4, "max_attempts": 15},
            "hard": {"num_digits": 5, "max_attempts": 12}
        }
        self.colors = ["🔴", "🔵", "🟢", "🟡", "🟣", "🟠", "🟤"]
        self.color_to_num = {color: str(i) for i, color in enumerate(self.colors)}
        self.num_to_color = {str(i): color for i, color in enumerate(self.colors)}

    def format_attempt(self, attempt):
        return "".join([self.num_to_color.get(num, num) for num in attempt])

    def generate_inline_markup_base(self):
        return self.create_keyboard("mm", "c", "delete", "submit")

    def create_keyboard(self, prefix, callback_prefix, del_prefix, sub_prefix) -> InlineKeyboardMarkup:
        keyboard = []
        row = []
        for i, color in enumerate(self.colors):
            num = self.color_to_num[color]
            row.append(InlineKeyboardButton(color, callback_data=f"{prefix}_{callback_prefix}_{num}"))
            if (i + 1) % 4 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)

        action_row = [
            InlineKeyboardButton("⌫", callback_data=f"{prefix}_{del_prefix}"),
            InlineKeyboardButton("⏎", callback_data=f"{prefix}_{sub_prefix}")
        ]
        keyboard.append(action_row)
        return InlineKeyboardMarkup(keyboard)

    def get_instructions(self, game):
        current_colors = self.format_attempt(game.current_guess)
        color_list = " ".join(self.colors)
        return (self._("Guess a {}-color combination (no repeats) using these colors: \n{}").format(game.num_digits, color_list) +
                f"\n\n" + self._("Current selection: {}").format(current_colors) +
                "\n\n" + self._("Results meaning:\n⚫: Correct color and position\n⚪: Correct color but wrong position\n❌: No matches"))

    async def make_attempt_logic(self, bot, user_id, attempt, name="Player", query=None, game=None):
        if game is None:
            game = self.get_game(user_id)
        
        game.check_number(attempt)
        text = game.template(
            self._("You have {} attempts left "), 
            self._("Results"),
            formatter=self.format_attempt
        )
        self.save_all_games()
        
        if game.is_winner():
            text += "\n\n" + self._("Congratulations, {}, YOU WON!!\n").format(name)
            if query:
                await query.edit_message_text(text)
            else:
                await self.send_message(bot, user_id, text)
        elif game.is_looser():
            solution = self.format_attempt("".join(game.numbers))
            text += "\n\n" + self._("I'm sorry, {}, YOU LOST!!\n The combination was {}").format(name, solution)
            if query:
                await query.edit_message_text(text)
            else:
                await self.send_message(bot, user_id, text)
        else:
            if query:
                await query.edit_message_text(text, reply_markup=self.generate_inline_markup(game))
            else:
                await self.send_message(bot, user_id, text, reply_markup=self.generate_inline_markup(game))

    def generate_inline_markup(self, game=None):
        raise NotImplementedError
