#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv

load_dotenv()

from games_bot import GamesTelegramBot
TOKEN_TELEGRAM = os.environ['TOKEN_TELEGRAM']
import re
pattern = re.compile(r"[-] [a-zA-ZáéíóúñÁÉÍÓÚÑ]+")
inline_pattern = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]+[_]+ [1-9]")

import threading
import http.server
import socketserver

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'Hello, world!')
        else:
            self.send_error(404)

PORT = 8080

def run_http_server():
    with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

if __name__ == '__main__':

    gamesBot = GamesTelegramBot("Classic Games Bot", TOKEN_TELEGRAM)
    gamesBot.handle_command("start", gamesBot.start)
    gamesBot.handle_command("games", gamesBot.display_games)
    gamesBot.handle_command("juegos", gamesBot.display_games)
    gamesBot.handle_query(gamesBot.select_game, pattern)
    gamesBot.handle_query(gamesBot.answer_button_by_game)
    gamesBot.handle_message(gamesBot.answer_message_by_game)
    gamesBot.handle_inline_mode(gamesBot.display_inline_games)

    http_thread = threading.Thread(target=run_http_server)
    http_thread.daemon = True
    http_thread.start()

    gamesBot.run()
