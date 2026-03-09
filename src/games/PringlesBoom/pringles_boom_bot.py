from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from base_bot import BotBase
from games.PringlesBoom.pringles_boom import PringlesBoomGame
from utils.errors import ModelError

class PringlesBoomBot(BotBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = PringlesBoomGame
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }

    def is_inline_game(self):
        return True

    def game_id(self):
        return '- pringles_boom'

    def name(self):
        return self._('Pringles Boom Challenge')

    def generate_inline_markup(self):
        # Initial board, all chips
        return self.generate_markup(self.Game())

    def generate_markup(self, game, user_id=None):
        # Rule 2: The bot should display two grids in one message.
        # Player A's Field (Target for B in PLAYING phase, Source for A in SETUP)
        # Player B's Field (Target for A in PLAYING phase, Source for B in SETUP)
        
        # Emoji representation:
        # Untouched: Chosen emoji (default 🥔)
        # Safe: ⭕
        # Bomb triggered: 💥
        # Bomb revealed (at end): 💣
        
        buttons = []
        
        if game.phase == game.PHASE_CHOOSING_EMOJI:
            # Show emoji selection buttons
            emojis = [ "🍏", "🍕", "🍪", "🍩", "🍣"]
            row = []
            for e in emojis:
                row.append(InlineKeyboardButton(e, callback_data=f"pb_emoji_{e}"))
            buttons.append([InlineKeyboardButton(self._("Choose your chip emoji:"), callback_data="pb_ignore")])
            buttons.append(row)
            return InlineKeyboardMarkup(buttons)

        # Helper to generate grid buttons
        def add_grid_to_buttons(grid, bombs, grid_num, is_finished, phase, owner_id):
            p1_emoji = game.player1_emoji
            p2_emoji = game.player2_emoji
            # Grid 1 owner is P1, Grid 2 owner is P2
            current_grid_emoji = p1_emoji if grid_num == 1 else p2_emoji

            for i in range(0, 9, 3):
                row = []
                for j in range(3):
                    idx = i + j
                    state = grid[idx]
                    
                    if phase == game.PHASE_SETUP:
                        # We NO LONGER show ⚠️ even to the owner because it's a shared inline message.
                        # Instead, we just show the chip emoji.
                        emoji = current_grid_emoji
                        callback_data = f"pb_pick_{grid_num}_{idx}"
                    elif state == 0:
                        if is_finished and idx in bombs:
                            emoji = "💣"
                            callback_data = "pb_ignore"
                        else:
                            emoji = current_grid_emoji
                            callback_data = f"pb_pick_{grid_num}_{idx}"
                    elif state == 1:
                        emoji = "⭕"
                        callback_data = "pb_ignore"
                    elif state == 2:
                        emoji = "💥"
                        callback_data = "pb_ignore"
                    
                    row.append(InlineKeyboardButton(emoji, callback_data=callback_data))
                buttons.append(row)

        # Add Header for Grid 1 (Player 1's field)
        buttons.append([InlineKeyboardButton(self._("--- {}'s Field ---").format(game.player1_name), callback_data="pb_ignore")])
        add_grid_to_buttons(game.grid1, game.bombs1, 1, game.game_finished, game.phase, game.player1_id)
        
        # Add Separator
        buttons.append([InlineKeyboardButton("-----------------------", callback_data="pb_ignore")])
        
        # Add Header for Grid 2 (Player 2's field)
        buttons.append([InlineKeyboardButton(self._("--- {}'s Field ---").format(game.player2_name), callback_data="pb_ignore")])
        add_grid_to_buttons(game.grid2, game.bombs2, 2, game.game_finished, game.phase, game.player2_id)

        return InlineKeyboardMarkup(buttons)

    async def answer_button(self, update, context):
        user_id = self.get_user_id(update)
        user_name = update.effective_user.first_name
        message_id = self.get_message_id(update)
        
        if message_id not in self.users_data:
            self.logger.info(f"User {user_name} ({user_id}) started inline game: {self.name()} ({message_id})")
            self.users_data[message_id] = self.Game(player1_id=user_id, player1_name=user_name)
        
        game = self.get_game(message_id)
        
        if game.finished():
            await self.game_finished_message(update, context)
            return

        query_data = update.callback_query.data
        if not query_data.startswith("pb_"):
            return
        
        if query_data == "pb_ignore":
            await update.callback_query.answer()
            return

        try:
            # format: pb_pick_{grid_num}_{idx}
            parts = query_data.split("_")
            if len(parts) == 4 and parts[1] == "pick":
                grid_num = int(parts[2])
                cell = int(parts[3])
                game.pick(user_id, cell, grid_num, user_name=user_name)
                
                # To solve visibility, we can send a private confirmation of where they placed the bomb
                if game.phase == game.PHASE_SETUP:
                    await update.callback_query.answer(self._("Action registered!"), show_alert=False)
                
                caption = self.get_game_status_message(game, context)
                await context.bot.edit_message_caption(
                    inline_message_id=message_id,
                    caption=caption,
                    reply_markup=self.generate_markup(game, user_id=user_id)
                )
                self.save_all_games()
            elif len(parts) == 3 and parts[1] == "emoji":
                emoji = parts[2]
                game.set_emoji(user_id, emoji)
                
                caption = self.get_game_status_message(game, context)
                await context.bot.edit_message_caption(
                    inline_message_id=message_id,
                    caption=caption,
                    reply_markup=self.generate_markup(game, user_id=user_id)
                )
                self.save_all_games()
            else:
                await update.callback_query.answer()
            
        except ModelError as e:
            # Snarky temporary alert (e.g., "Wait your turn! ✋")
            await update.callback_query.answer(self._(e.message), show_alert=True)
        except Exception as e:
            self.logger.error(f"Error in PringlesBoomBot.answer_button: {e}")
            await update.callback_query.answer(self._("An error occurred."))

    def get_game_status_message(self, game, context):
        if game.phase == game.PHASE_SETUP:
            p1_bombs = len(game.bombs1)
            p2_bombs = len(game.bombs2)
            return self._("Setup Phase: Place 3 bombs on your board!\n{}: {}/3, {}: {}/3").format(
                game.player1_name, p1_bombs, game.player2_name, p2_bombs)

        if game.phase == game.PHASE_CHOOSING_EMOJI:
            p1_ready = "✅" if game.player1_emoji != "🥔" else "⏳"
            p2_ready = "✅" if game.player2_emoji != "🥔" else "⏳"
            return self._("Choose your emoji!\n{}: {}, {}: {}").format(
                game.player1_name, p1_ready, game.player2_name, p2_ready)

        if game.game_finished:
            winner_name = game.player1_name if game.winner_id == game.player1_id else game.player2_name
            return self._("Game Over! {} wins!").format(winner_name)
        
        current_player = game.player1_name if game.turn == 1 else game.player2_name
        return self._("Turn: {}. Pick a chip from the opponent's grid!").format(current_player)
