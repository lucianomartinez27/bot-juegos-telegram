from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from base_bot import BotBase
from games.TicTacToe.tictactoe import TicTacToeGame
from games.TicTacToe.tictactoe_bot import generate_markup


class BotTaTeTiInLine(BotBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = TicTacToeGame
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }

    def is_inline_game(self):
        return True

    def game_id(self):
        return '- tictactoe_multiplayer'

    def name(self):
        return self._('Tic-Tac-Toe MultiPlayer')

    def generate_inline_markup(self):
        options = [[InlineKeyboardButton(" ", callback_data="{}".format(i))
                     for i in j] for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
        return InlineKeyboardMarkup(options)
    
    def get_player_symbols(self, game, context):
        return [context.user_data["player_symbol"], context.user_data["opposite_symbol"]]
    
    async def answer_button(self, update, context):
        user_id = self.get_user_id(update)
        self.users_data.setdefault(self.get_message_id(update), self.generate_game_state(user_id))
        message_id = self.get_message_id(update)
        game = self.get_game(message_id)
        self.reset_player_symbols(context, game)
       
        cell = int(update.callback_query.data)
        bot = context.bot
        game = self.get_game(message_id)

        [player_symbol, opposite_symbol] = self.get_player_symbols(game, context)

        if game.finished():
            await self.game_finished_message(update, context)
        else:
            game.mark_cell(player_symbol, cell)
            if not game.finished():
                self.make_opponent_movement(game)
            await self.update_board(bot, game, None, message_id)
            if game.finished():
                context.user_data["player_symbol"] = None
                context.user_data["opposite_symbol"] = None
                if game.is_winner(player_symbol):
                    await context.bot.edit_message_caption(inline_message_id=message_id, caption= player_symbol + self._(' won'), reply_markup=self.generate_markup(game))
                elif game.is_winner(opposite_symbol):
                    await context.bot.edit_message_caption(inline_message_id=message_id, caption= opposite_symbol + self._(' won'), reply_markup=self.generate_markup(game))
                else: #isTie
                    await context.bot.edit_message_caption(inline_message_id=message_id, caption= self._('Was a tie'), reply_markup=self.generate_markup(game))
            self.save_all_games()

    def reset_player_symbols(self, context, game):
        if game.no_movement_done():
            context.user_data["player_symbol"] = 'X'
            context.user_data["opposite_symbol"] = 'O'
        elif game.just_one_movement_done() and not (context.user_data.get("player_symbol") == 'X'):
            context.user_data["player_symbol"] = 'O'
            context.user_data["opposite_symbol"] = 'X'
    
    async def update_board(self, bot, game, chat_id, message_id):
        return await bot.edit_message_reply_markup(chat_id=chat_id,
                                             message_id=None,
                                             inline_message_id=message_id,
                                             reply_markup=generate_markup(game))
    
    def make_opponent_movement(self, game):
        pass # just wait for the opponent
       
