from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from games.TicTacToe.tictactoe_bot import BotTicTacToe
from games.TicTacToe.tictactoe import TicTacToeGame


class BotTaTeTiInLine(BotTicTacToe):
    def __init__(self):
        super(BotTicTacToe, self).__init__(__file__)
        self.Game = TicTacToeGame
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }

    def is_inline_game(self):
        return True

    def name(self):
        return 'TaTeTi_MultiPlayer'

    def generate_markup(self, update, context):
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
        if not context.user_data.get("player_symbol"):
            if game.no_movement_done():
                context.user_data["player_symbol"] = 'X'
                context.user_data["opposite_symbol"] = 'O'
            elif game.just_one_movement_done():
                context.user_data["player_symbol"] = 'O'
                context.user_data["opposite_symbol"] = 'X'
       
        cell = int(update.callback_query.data)
        bot = context.bot
        game = self.get_game(message_id)

        [player_symbol, opposite_symbol] = self.get_player_symbols(game, context)

        if game.finished():
            await self.game_finished_message(bot, user_id)
        else:
            game.mark_cell(player_symbol, cell)            
            if not game.finished():
                self.make_opponent_movement(game)

            if game.finished():
                if game.is_winner(player_symbol):
                    await self.send_message(bot, user_id, 'Ganaste')
                elif game.is_winner(opposite_symbol):
                    await self.send_message(bot, user_id, 'Perdiste')
                else: #isTie
                    await self.send_message(bot, user_id, 'Empataste')
            self.save_all_games()
            await self.update_board(bot, game.board, user_id, message_id)
    
    def update_board(self, bot, board, chat_id=None, message_id=None, id_mensaje_inline=None):
        return super().update_board(bot, board, None, None, message_id)
    
    def make_opponent_movement(self, game):
        pass # just wait for the opponent
       
