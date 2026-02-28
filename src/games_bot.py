#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
from telegram_bot import BotTelegram
from games.Hangman.hangman_bot import BotTelegramAhorcado
from games.Hangman.hangman_multiplayer_bot import BotHangmanMultiPlayer
from games.Mastermind.bot_mastermind import BotMastermind
from games.Minesweeper.minesweeper_bot import BotBuscaminas
from games.TicTacToe.tictactoe_bot import BotTicTacToe
from games.TicTacToe_MultiPlayer.inline_tictactoe_bot import BotTaTeTiInLine
from games.RockPaperScissor.rock_paper_scissor_bot import BotRockPaperScissor
from games.RockPaperScissor.rock_paper_scissor_multiplayer_bot import BotRockPaperScissorMultiplayer
from utils.data_manager import DataManager
from telegram import InputTextMessageContent, InlineQueryResultArticle
from uuid import uuid4

import os

# Para crear boton en telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

bot_mastermind = BotMastermind()
bot_tictactoe = BotTicTacToe()
bot_ahorcado = BotTelegramAhorcado()
bot_buscaminas = BotBuscaminas()
bot_rps = BotRockPaperScissor()
bot_tateti_inline = BotTaTeTiInLine()
bot_hangman_multiplayer = BotHangmanMultiPlayer()
bot_rps_multiplayer = BotRockPaperScissorMultiplayer()
from internationalization import set_translator, _, spanish

from functools import wraps

def ensure_session(func):
    @wraps(func)
    async def wrapped(self, update, context, *pargs, **kwargs):
        user_id = self.get_user_id(update)
        self.ensure_user_data(user_id)
        return await func(self, update, context, *pargs, **kwargs)
    return wrapped

def game_session(func):
    """Decorator that ensures user session data is initialized and sets the translator."""
    return set_translator(ensure_session(func))

class GamesTelegramBot(BotTelegram):
    def __init__(self, name, token):
        """Initializes bot; populates game catalog; manages user data"""
        BotTelegram.__init__(self, name, token)
        self.game_catalog = {game.game_id(): game for game in [
            bot_ahorcado,
            bot_buscaminas,
            bot_mastermind,
            bot_tictactoe,
            bot_tateti_inline,
            bot_hangman_multiplayer,
            bot_rps,
            bot_rps_multiplayer
        ]}
        
        self.data_manager = DataManager(os.path.abspath(''))
        self.user_data = self.data_manager.generate_info(dict())
    
    def get_game_bot(self, game_id):
        return self.game_catalog.get(game_id)
    
    # TO-DO: We should re check how this is done
    def change_translator(self, new_translator, language_code):
        super().change_translator(new_translator, language_code)
        for game in self.game_catalog.values():
            game.change_translator(new_translator, language_code)
    
    def ensure_user_data(self, user_id):
        user_id_str = str(user_id)
        if user_id_str not in self.user_data:
            self.user_data[user_id_str] = {"juego_actual": None, "estado": {}, "language": None}
            self.data_manager.save_info(self.user_data)
        elif "language" not in self.user_data[user_id_str]:
            self.user_data[user_id_str]["language"] = None
            self.data_manager.save_info(self.user_data)

    @set_translator
    async def start(self, update, context):
        bot = context.bot
        user_id = self.get_user_id(update)
        user_name = update.message.chat.first_name
        if str(user_id) not in self.user_data:
            self.user_data[str(user_id)] = {"juego_actual": None, "estado": {}, "language": None}
        self.data_manager.save_info(self.user_data)
        message = self._("Hello *{}*, welcome to classic games bot. Use /games to show the available games").format(user_name) + ".\n\n"
        message += self._("There are also some multiplayer games. To play them, you have to write `@the_classic_games_bot play` on your friend's chat.") + "\n\n"
        message += self._("A list with the available games will be shown, then select the game that you want to play.")
        await self.send_message(bot, user_id, message, 'markdown')

    @game_session
    async def display_games(self, update, context):
        games = [[InlineKeyboardButton(game.name(), callback_data=game.game_id())] for game in
                    self.game_catalog.values() if not game.is_inline_game()]
        await update.message.reply_text(self._("Available games are:"), reply_markup=InlineKeyboardMarkup(games))

    @game_session
    async def display_languages(self, update, context):
        languages = [
            [InlineKeyboardButton("English 🇬🇧", callback_data="lang_en")],
            [InlineKeyboardButton("Español 🇪🇸", callback_data="lang_es")]
        ]
        await update.message.reply_text(self._("Select your language:"), reply_markup=InlineKeyboardMarkup(languages))

    async def set_language(self, update, context):
        query = update.callback_query
        user_id = str(self.get_user_id(update))
        lang_code = query.data.split("_")[1]
        
        self.user_data[user_id]["language"] = lang_code
        self.data_manager.save_info(self.user_data)
        
        # Apply the new translator for the confirmation message
        if lang_code == "es":
            new_translator = spanish.gettext
            confirmation = self._("Idioma cambiado a Español 🇪🇸")
        else:
            new_translator = _
            confirmation = self._("Language changed to English 🇬🇧")
        
        self.change_translator(new_translator, lang_code)
            
        await query.answer()
        await query.edit_message_text(text=confirmation)

    def get_inline_game_by_query_data(self, query_data):
        if query_data in ['scissors', 'rock', 'paper']:
            return bot_rps_multiplayer.game_id()
        elif query_data.startswith("h_"):
            return bot_hangman_multiplayer.game_id()
        else:
            return bot_tateti_inline.game_id()

    @game_session
    async def display_inline_games(self, update, context):
        inline_games = []
        for bot_game in self.game_catalog.values():
            if bot_game.is_inline_game():
                inline_message_id = uuid4()
                inline_games.append(InlineQueryResultArticle(
                    id=str(inline_message_id),
                    title=bot_game.name(),
                    input_message_content=InputTextMessageContent(self._("Let's play to: {}").format(bot_game.name())),
                    reply_markup=bot_game.generate_inline_markup()))
        self.data_manager.save_info(self.user_data)

        await update.inline_query.answer(inline_games)
    
    @game_session
    async def select_game(self, update, context):
        selected_game_id = update.callback_query.data
        user = self.get_user_id(update)
        bot = context.bot
        self.user_data[str(user)]["juego_actual"] = selected_game_id
        self.data_manager.save_info(self.user_data)

        game_bot = self.get_game_bot(selected_game_id)
        await self.send_message(bot, user, self._("You chose to play {}. To change the game, you can use /games again") \
                            .format(game_bot.name()))

        await game_bot.play(update, context)

    @game_session
    async def answer_button_by_game(self, update, context):
        query = update.callback_query
        if query.data.startswith("lang_"):
            return await self.set_language(update, context)

        if not query.inline_message_id:
            return await self.run_current_game_if_available(update, context, True)
        else:
            game_id = self.get_inline_game_by_query_data(query.data)
            return await self.get_game_bot(game_id).answer_button(update, context)
    
    @game_session
    async def answer_message_by_game(self, update, context):
        await self.run_current_game_if_available(update, context)

    async def run_current_game_if_available(self, update, context, is_button_message=False):
        # TODO: Do not use boolean flag for button messages
        user_id = self.get_user_id(update)
        current_game_id = self.user_data[str(user_id)]["juego_actual"]
        if current_game_id:
            game_bot = self.get_game_bot(current_game_id)
            if is_button_message:
                await game_bot.answer_button(update, context)
            else:
                 await game_bot.answer_message(update, context)
        else:
            await self.send_message(context.bot, user_id,
            self._("You don't have an active game. Use /games to start one."))

