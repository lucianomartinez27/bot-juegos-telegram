#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bot_juegos import BotDeJuegosTelegram
from config.keys import TOKEN_TELEGRAM

if __name__ == '__main__':
    bot_juegos = BotDeJuegosTelegram("BotAhorcado", TOKEN_TELEGRAM)
    bot_juegos.esperar_comando("start", bot_juegos.start)
    bot_juegos.esperar_comando("juegos", bot_juegos.juegos)
    bot_juegos.contestar_consulta(bot_juegos.seleccionar_juego)
    bot_juegos.contestar_mensaje(bot_juegos.responder_mensaje_segun_juego)
