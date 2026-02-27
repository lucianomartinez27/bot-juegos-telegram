#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base_bot import BotBase
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .minesweeper import Minesweeper


class BotBuscaminas(BotBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = Minesweeper
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }
        self.difficulty_settings = {
            "easy": {"rows": 8, "cols": 8, "bombs": 8},
            "medium": {"rows": 10, "cols": 10, "bombs": 15},
            "hard": {"rows": 12, "cols": 12, "bombs": 25}
        }

    def game_id(self):
        return '- minesweeper'

    def name(self):
        return '- Minesweeper'

    async def play(self, update, context):
        difficulties = [
            [InlineKeyboardButton(self._("Easy"), callback_data="ms_diff_easy")],
            [InlineKeyboardButton(self._("Medium"), callback_data="ms_diff_medium")],
            [InlineKeyboardButton(self._("Hard"), callback_data="ms_diff_hard")]
        ]
        
        await update.callback_query.message.reply_text(
            self._("Select difficulty level:"), 
            reply_markup=InlineKeyboardMarkup(difficulties)
        )

    async def answer_button(self, update, context):
        query = update.callback_query
        if query.data.startswith("ms_diff_"):
            difficulty = query.data.split("_")[2]
            user_id = self.get_user_id(update)
            settings = self.difficulty_settings[difficulty]
            self.generate_game_state(user_id, settings["rows"], settings["cols"], settings["bombs"])
            game = self.get_game(user_id)
            await query.edit_message_text(
                self._('Minesweeper:'), 
                reply_markup=InlineKeyboardMarkup(self.board_markup(game))
            )
            return

        row, col = update.callback_query.data.split()
        bot = context.bot
        user_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id
        game = self.get_game(user_id)
        if game.finished():
            await self.game_finished_message(bot, user_id)
        else:
            game.mark_cell(int(row), int(col))
            self.save_all_games()
            await bot.edit_message_reply_markup(chat_id=user_id, message_id=message_id,
                                            reply_markup=InlineKeyboardMarkup(self.board_markup(game)))
            if game.finished():
                if game.is_winner():
                    await self.send_message(bot, user_id,  self._("You won"))
                else:
                    await self.send_message(bot, user_id,  self._("You lost"))


    def generate_game_state(self, user_id, rows=8, cols=8, bombs=8):
        self.users_data[str(user_id)] = self.Game(rows, cols, bombs)
        self.save_all_games()
        return self.users_data[str(user_id)]

    def board_markup(self, game):
         return [
            [InlineKeyboardButton(game.board()[col][row], callback_data="{} {}".format(col, row)) for row in range(game.num_of_rows)]
            for col in range(game.num_of_cols)
        ]