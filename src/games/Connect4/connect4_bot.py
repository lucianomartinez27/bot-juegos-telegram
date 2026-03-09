#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.errors import ModelError
from base_bot import BotBase
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from .connect4 import AgainstComputerConnect4

def generate_markup(game):
    # Only one row of buttons for columns 0-6
    row_buttons = [InlineKeyboardButton(str(c + 1), callback_data="c4_{}".format(c)) for c in range(game.cols)]
    return InlineKeyboardMarkup([row_buttons])

def generate_board_text(game):
    # Create the text board display
    board_text = ""
    for r in range(game.rows):
        row_str = ""
        for c in range(game.cols):
            symbol = game.board[r][c]
            if symbol == " ":
                display_symbol = "⚪"
            else:
                display_symbol = symbol
            row_str += display_symbol
        board_text += row_str + "\n"
    
    # Add column numbers at the bottom for easier reference
    board_text += "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣"
    return board_text

class BotConnect4(BotBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = AgainstComputerConnect4
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }
    
    def game_id(self):
        return '- connect4'

    def name(self):
        return '- Connect 4'

    async def play(self, update, context):
        user_id = self.get_user_id(update)
        user_name = update.effective_user.first_name
        self.logger.info(f"User {user_name} ({user_id}) started game: {self.name()}")
        bot = context.bot
        self.generate_game_state(user_id)
        # Choosing side: Red or Yellow
        custom_keyboard = [['🔴', '🟡']]
        await bot.send_message(chat_id=user_id,
                         text=self._("Please choose your side:"),
                         reply_markup=ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True))

    async def generate_board(self, update, game):
        await update.message.reply_text(generate_board_text(game), reply_markup=generate_markup(game))

    async def answer_message(self, update, context):
        user_id = self.get_user_id(update)
        game = self.get_game(user_id)
        if not game.started() and update.message:
            symbol = update.message.text
            if symbol not in ['🔴', '🟡']:
                await update.message.reply_text(self._("Please choose 🔴 or 🟡"))
                return
            game.player_symbol = symbol
            game.computer_symbol = '🟡' if symbol == '🔴' else '🔴'
            # We can decide who starts. Let's say player starts if they choose 🔴
            if game.computer_symbol == '🔴':
                game.make_computer_movement()
            await self.generate_board(update, game)
        elif update.callback_query:
            await self.answer_button(update, context)

    async def update_board(self, bot, game, chat_id, message_id):
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=message_id,
                                    text=generate_board_text(game),
                                    reply_markup=generate_markup(game))

    def get_player_symbols(self, game, context):
        return [game.player_symbol, game.computer_symbol]

    async def answer_button(self, update, context):
        bot = context.bot
        user_id = self.get_user_id(update)
        user_name = update.effective_user.first_name
        message_id = self.get_message_id(update)
        if str(user_id) not in self.users_data:
            self.logger.info(f"User {user_name} ({user_id}) started game: {self.name()}")
            self.generate_game_state(user_id)
        
        game = self.get_game(user_id)

        [player_symbol, computer_symbol] = self.get_player_symbols(game, context)

        if game.finished():
            await self.game_finished_message(update, context)
        else:
            try:
                # Remove c4_ prefix
                col_data = update.callback_query.data
                if col_data.startswith("c4_"):
                    col = int(col_data.split("_")[1])
                else:
                    col = int(col_data)

                game.mark_column(player_symbol, col)
                if not game.finished():
                    game.make_computer_movement()
                
                if game.finished():
                    if game.winner == player_symbol:
                        await self.send_message(bot, user_id, self._('You won'))
                    elif game.winner == computer_symbol:
                        await self.send_message(bot, user_id, self._('You lost'))
                    else: #isTie
                        await self.send_message(bot, user_id, self._('Was a tie'))
                
                self.save_all_games()
                await self.update_board(bot, game, user_id, message_id)
            except ModelError as e:
                await update.callback_query.answer(self._(e.message), show_alert=True)
