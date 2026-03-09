from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from base_bot import BotBase
from games.Connect4.connect4 import Connect4Game
from games.Connect4.connect4_bot import generate_markup, generate_board_text


class BotConnect4InLine(BotBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = Connect4Game
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }

    def is_inline_game(self):
        return True

    def game_id(self):
        return '- connect4_multiplayer'

    def name(self):
        return self._('Connect 4 MultiPlayer')

    def generate_inline_markup(self):
        game = self.Game() # Temporary game to use its dimensions
        return generate_markup(game)

    def get_inline_initial_message(self):
        game = self.Game()
        return generate_board_text(game)
    
    def get_player_symbols(self, game, context):
        return [context.user_data["player_symbol"], context.user_data["opposite_symbol"]]
    
    async def answer_button(self, update, context):
        user_id = self.get_user_id(update)
        user_name = update.effective_user.first_name
        message_id = self.get_message_id(update)
        if message_id not in self.users_data:
            self.logger.info(f"User {user_name} ({user_id}) started inline game: {self.name()} ({message_id})")
            self.users_data[message_id] = self.generate_game_state(message_id)
        
        game = self.get_game(message_id)
        self.reset_player_symbols(context, game)
       
        # Remove c4_ prefix
        col_data = update.callback_query.data
        if col_data.startswith("c4_"):
            col = int(col_data.split("_")[1])
        else:
            col = int(col_data)
        
        bot = context.bot
        
        [player_symbol, opposite_symbol] = self.get_player_symbols(game, context)

        if game.finished():
            await self.game_finished_message(update, context)
        else:
            try:
                game.mark_column(player_symbol, col)
                # In multiplayer, we don't make an automatic opponent movement
                
                await self.update_board(bot, game, None, message_id)
                
                if game.finished():
                    context.user_data["player_symbol"] = None
                    context.user_data["opposite_symbol"] = None
                    caption = ""
                    if game.winner == player_symbol:
                        caption = player_symbol + self._(' won')
                    elif game.winner == opposite_symbol:
                        caption = opposite_symbol + self._(' won')
                    else: #isTie
                        caption = self._('Was a tie')
                    
                    await context.bot.edit_message_caption(inline_message_id=message_id, 
                                                           caption=generate_board_text(game) + "\n\n" + caption, 
                                                           reply_markup=generate_markup(game))
                self.save_all_games()
            except Exception as e:
                # Could be ModelError or something else
                from utils.errors import ModelError
                if isinstance(e, ModelError):
                    await update.callback_query.answer(self._(e.message), show_alert=True)
                else:
                    raise e

    def reset_player_symbols(self, context, game):
        if game.no_movement_done():
            context.user_data["player_symbol"] = '🔴'
            context.user_data["opposite_symbol"] = '🟡'
        elif game.just_one_movement_done() and not (context.user_data.get("player_symbol") == '🔴'):
            context.user_data["player_symbol"] = '🟡'
            context.user_data["opposite_symbol"] = '🔴'
    
    async def update_board(self, bot, game, chat_id, message_id):
        return await bot.edit_message_caption(chat_id=chat_id,
                                             message_id=None,
                                             inline_message_id=message_id,
                                             caption=generate_board_text(game),
                                             reply_markup=generate_markup(game))
