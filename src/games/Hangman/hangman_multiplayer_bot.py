from .hangman_base_bot import BotHangmanBase
from .multiplayer_hangman import MultiPlayerHangManGame


class BotHangmanMultiPlayer(BotHangmanBase):
    def __init__(self):
        super().__init__(__file__)
        self.Game = MultiPlayerHangManGame
        self.users_data = { key: self.Game.from_json(value) for key, value in self.users_data.items() }

    def is_inline_game(self):
        return True

    def game_id(self):
        return '- hangman_multiplayer'

    def name(self):
        return self._('Hangman MultiPlayer')

    async def send_keyboard(self, caption, update, context, game, message_id):
        await context.bot.edit_message_text(
            inline_message_id=message_id,
            text=f"<pre>\n{caption}\n</pre>",
            reply_markup=self.generate_inline_markup(game),
            parse_mode='HTML'
        )

