from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from games.TicTacToe.tictactoe_bot import BotTicTacToe


class BotTaTeTiInLine(BotTicTacToe):
    def __init__(self):
        super(BotTicTacToe, self).__init__(__file__)

    def is_inline_game(self):
        return True

    def name(self):
        return 'TaTeTi_MultiPlayer'

    def generate_game_state(self, user_id):
        # user_id se convierte en string porque las claves json deben ser de ese tipo
        return {'users': {user_id: {'player_symbol': 'X'}}, 'board': [" " for i in range(9)],
                'game_finished': False}

    def generate_markup(self, update, context):
        options = [[InlineKeyboardButton(" ", callback_data="{}".format(i))
                     for i in j] for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
        return InlineKeyboardMarkup(options)

    async def answer_button(self, update, context):
        square = int(update.callback_query.data)
        user_id = str(self.get_user_id(update))
        bot = context.bot
        inline_message_id = self.get_message_id(update)
        self.users_data.setdefault(inline_message_id, self.generate_game_state(user_id))
        self.data_manager.save_info(self.users_data)
        self.assign_symbol_to_opponent(inline_message_id, user_id)

        letra = self.users_data[inline_message_id]['users'][user_id]['player_symbol']
        board = self.users_data[inline_message_id]['board']
        await self.mark_square(bot, square, user_id, inline_message_id, letra, board)

    async def mark_square(self, bot, casilla, user_id, message_id, letra, board):
        if self.is_players_turn(letra, board):
            board[casilla] = letra
            await self.update_board(bot, board, None, None, message_id)

    def is_players_turn(self, letra, board):
        return letra == 'X' and board.count(' ') % 2 != 0 or \
               board.count(' ') % 2 == 0 and letra == 'O'

    def assign_symbol_to_opponent(self, message_id, user_id):
        if self.there_has_been_just_one_movement(message_id):
            self.users_data[message_id]['users'].update({user_id: {'player_symbol': 'O'}})

    def there_has_been_just_one_movement(self, message_id):
        return self.users_data[message_id]['board'].count('X') == 1 and \
               self.users_data[message_id]['board'].count('O')
