#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bot_ahorcado import BotTelegramAhorcado
from config.keys import TOKEN_TELEGRAM

if __name__ == '__main__':
    bot_ahorcado = BotTelegramAhorcado("BotAhorcado", TOKEN_TELEGRAM)
    bot_ahorcado.esperar_comando("start", bot_ahorcado.start)
    bot_ahorcado.esperar_comando("jugar", bot_ahorcado.jugar)
    bot_ahorcado.contestar_mensaje(bot_ahorcado.elegir_letra)