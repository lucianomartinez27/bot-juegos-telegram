#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

from games_bot import GamesTelegramBot
TOKEN_TELEGRAM = os.environ['TOKEN_TELEGRAM']
BOT_NAME = os.environ.get('BOT_NAME', 'PlayTheGamesBot')
BOT_USERNAME = os.environ.get('BOT_USERNAME', 'PlayTheGamesBot')
import re
pattern = re.compile(r"[-] [a-zA-ZáéíóúñÁÉÍÓÚÑ ,]+")
inline_pattern = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ ,]+[_]+ [1-9]")

if __name__ == '__main__':

    gamesBot = GamesTelegramBot(BOT_NAME, TOKEN_TELEGRAM, BOT_USERNAME)
    gamesBot.handle_command("start", gamesBot.start)
    gamesBot.handle_command("games", gamesBot.display_games)
    gamesBot.handle_command("juegos", gamesBot.display_games)
    gamesBot.handle_command("language", gamesBot.display_languages)
    gamesBot.handle_command("idiomas", gamesBot.display_languages)
    gamesBot.handle_query(gamesBot.select_game, pattern)
    gamesBot.handle_query(gamesBot.answer_button_by_game)
    gamesBot.handle_message(gamesBot.answer_message_by_game)
    gamesBot.handle_inline_mode(gamesBot.display_inline_games)

    WEBHOOK_URL = os.getenv('WEBHOOK_URL')

    if WEBHOOK_URL:
        PORT = int(os.getenv('PORT', 8080))
        # Secret token is recommended for webhooks
        SECRET_TOKEN = os.getenv('WEBHOOK_SECRET_TOKEN')
        gamesBot.run_webhook(WEBHOOK_URL, PORT, SECRET_TOKEN)
    else:
        gamesBot.run()
