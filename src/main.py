#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from bot_juegos import BotDeJuegosTelegram
TOKEN_TELEGRAM = os.environ['TOKEN_TELEGRAM']
import re
patron = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]+")
patron_inline = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]+[_]+ [1-9]")

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

PORT = 8000

with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()

if __name__ == '__main__':
    bot_juegos = BotDeJuegosTelegram("BotAhorcado", TOKEN_TELEGRAM)
    bot_juegos.handle_command("start", bot_juegos.start)
    bot_juegos.handle_command("juegos", bot_juegos.mostrar_juegos)
    bot_juegos.handle_query(bot_juegos.seleccionar_juego, patron)
    bot_juegos.handle_query(bot_juegos.responder_boton_segun_juego)
    bot_juegos.handle_message(bot_juegos.responder_mensaje_segun_juego)
    bot_juegos.handle_inline_mode(bot_juegos.mostrar_juegos_inline)
    bot_juegos.run()
