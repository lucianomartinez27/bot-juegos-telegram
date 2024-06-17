#!/usr/bin/env/python3
# -*- coding: utf-8 -*-

from telegram_bot import BotTelegram
from games.Hangman.hangman_bot import BotTelegramAhorcado
from games.Mastermind.bot_mastermind import BotMastermind
from games.Minesweeper.minesweeper_bot import BotBuscaminas
from games.TicTacToe.tictactoe_bot import BotTicTacToe
from games.TicTacToe_MultiPlayer.inline_tictactoe_bot import BotTaTeTiInLine
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

bot_tateti_inline = BotTaTeTiInLine()


class BotDeJuegosTelegram(BotTelegram):
    def __init__(self, name, token):
        BotTelegram.__init__(self, name, token)
        self.game_catalog = {bot_ahorcado.name(): bot_ahorcado,
                                   bot_buscaminas.name(): bot_buscaminas,
                                   bot_mastermind.name(): bot_mastermind,
                                   bot_tictactoe.name(): bot_tictactoe,
                                   bot_tateti_inline.name(): bot_tateti_inline}
        self.data_manager = DataManager(os.path.abspath(''))
        self.user_data = self.data_manager.generate_info(dict())

    async def start(self, update, context):
        bot = context.bot
        user_id = self.get_user_id(update)
        user_name = update.message.chat.first_name
        self.user_data[str(user_id)] = {"juego_actual": None, "estado": {}}
        self.data_manager.save_info(self.user_data)
        self.send_message(bot, user_id, "Hola {}, bienvenido al bot de juegos. Utiliza /juegos para\
        ver la lista de juegos.".format(user_name))

    async def display_games(self, update, context):
        games = [[InlineKeyboardButton(game.name(), callback_data=game.name())] for game in
                    self.game_catalog.values() if not game.is_inline_game()]
        await update.message.reply_text('Los juegos disponibles son:', reply_markup=InlineKeyboardMarkup(games))
        self.logger.info("Se ha iniciado un nuevo juego")

    async def display_inline_games(self, update, context):
        inline_games = []
        for bot_game in self.game_catalog.values():
            if bot_game.is_inline_game():
                inline_games.append(InlineQueryResultArticle(
                    id=uuid4(),
                    title=bot_game.name(),
                    input_message_content=InputTextMessageContent('Vamos a jugar a {}'.format(bot_game.name())),
                    reply_markup=bot_game.generate_inline_markup()))
        user_id = self.get_user_id(update)
        self.user_data[str(user_id)] = {'juego_actual': 'TaTeTi_MultiPlayer'}
        self.data_manager.save_info(self.user_data)

        await update.inline_query.answer(inline_games)

    async def select_game(self, update, context):
        selected_game = update.callback_query.data
        user = self.get_user_id(update)
        bot = context.bot
        self.user_data[str(user)] = {"juego_actual": selected_game}
        self.data_manager.save_info(self.user_data)

        await self.send_message(bot, user, "Elegiste jugar al {}. Para cambiar de juego puedes usar /juegos nuevamente." \
                            .format(selected_game))

        await self.game_catalog[selected_game].play(update, context)

    async def answer_button_by_game(self, update, context):
        try:
            user = self.get_user_id(update)
            current_game = self.user_data[str(user)]["juego_actual"]
            await self.game_catalog[current_game].answer_button(update, context)
        except KeyError:
            # Solucionar luego este hardcodeo
            await self.game_catalog['TaTeTi_MultiPlayer'].answer_button(update, context)

    async def answer_message_by_game(self, update, context):
        user_id = self.get_user_id(update)
        current_game = self.user_data[str(user_id)]["juego_actual"]
        await self.game_catalog[current_game].answer_message(update, context)

