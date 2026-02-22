#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from base_bot import BotBase
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .minesweeper import Minesweeper


class BotBuscaminas(BotBase):
    def __init__(self):
        super(BotBuscaminas, self).__init__(__file__)
        self.Game = Minesweeper
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }

    def name(self):
        return '- Minesweeper'

    async def play(self, update, context):
        user_id = update.callback_query.message.chat_id
        self.generate_game_state(user_id)
        game = self.get_game(user_id)

        await update.callback_query.message.reply_text(self._('Minesweeper:'), reply_markup=InlineKeyboardMarkup(self.board_markup(game)))

    async def answer_button(self, update, context):
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


    def board_markup(self, game):
         return [
            [InlineKeyboardButton(game.board()[col][row], callback_data="{} {}".format(col, row)) for row in range(game.num_of_rows)]
            for col in range(game.num_of_cols)
        ]