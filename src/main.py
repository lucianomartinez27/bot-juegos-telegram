#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.bot_juegos import BotDeJuegosTelegram
from src.config.keys import TOKEN_TELEGRAM
import re
patron = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ]+")

if __name__ == '__main__':
    bot_juegos = BotDeJuegosTelegram("BotAhorcado", TOKEN_TELEGRAM)
    bot_juegos.esperar_comando("start", bot_juegos.start)
    bot_juegos.esperar_comando("juegos", bot_juegos.mostrar_juegos)
    bot_juegos.contestar_consulta(bot_juegos.seleccionar_juego, patron)
    bot_juegos.contestar_consulta(bot_juegos.responder_boton_segun_juego)

    bot_juegos.contestar_mensaje(bot_juegos.responder_mensaje_segun_juego)
