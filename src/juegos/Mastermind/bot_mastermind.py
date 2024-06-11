#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Juego : MUERTOS Y HERIDOS - MASTERMIND
"""

from bot_base import BotBase
from juegos.Mastermind.funciones import generar_numero, comprobar_numero \
, chequear_numero, partida_ganada, partida_perdida
import os

class BotMastermind(BotBase):
    def __init__(self):
        super(BotMastermind, self).__init__(__file__)

    def name(self):
        return 'Mastermind'

    def generate_game_state(self, user_id):
        # user_id se convierte en string porque las claves json deben ser de ese tipo
        self.users_data[str(user_id)] = {}
        self.users_data[str(user_id)]['numeros_computadora'] = generar_numero()
        self.users_data[str(user_id)]['lista_resultados'] = []
        self.users_data[str(user_id)]['lista_intentos'] = []
        self.users_data[str(user_id)]['game_finished'] = False
        self.data_manager.save_info(self.users_data)

    async def play(self, update, context):
        user_id = update.callback_query.message.chat_id
        bot = context.bot
        self.generate_game_state(user_id)
        await self.send_message(bot, user_id, 'MUERTOS Y HERIDOS (MASTERMIND)')
        await self.send_message(bot, user_id,
                            'Adivina un número de 4 dígitos, si aciertas el número, pero no la posición\n'
                            'tienes un herido. Si aciertas el número y su posición tienes un muerto.')
        await self.send_message(bot, user_id, 'Para ganar necesitas conseguir 4 muertos. Tendrás 15 intentos.')

    async def answer_message(self, update, context):
        mensaje = update.message.text
        bot = context.bot
        user_id = update.message.chat_id
        name = update.message.chat.first_name

        numeros_computadora = self.users_data[str(user_id)]['numeros_computadora']
        lista_resultados = self.users_data[str(user_id)]['lista_resultados']
        lista_intentos = self.users_data[str(user_id)]['lista_intentos']

        if not self.users_data[str(user_id)]['game_finished']:
            if partida_ganada(mensaje, numeros_computadora):
                await self.send_message(bot, user_id, "Felicidades, {}, GANASTE!!\n "\
                                    .format(name))
                await self.send_message(bot, user_id, "Para cambiar de juego, usa /juegos.")
                self.users_data[str(user_id)]['game_finished'] = True
            elif partida_perdida(lista_intentos):
                await self.send_message(bot, user_id, "Lo siento, {}, PERDISTE!!\n El número era {}".format(name, "".join(numeros_computadora)))
                await self.send_message(bot, user_id, "Para cambiar de juego, usa /juegos.")
                self.users_data[str(user_id)]['game_finished'] = True
            else:
                if comprobar_numero(mensaje, lista_intentos):
                    await self.send_message(bot, user_id,
                                        chequear_numero(numeros_computadora, mensaje, lista_intentos, lista_resultados))
                else:
                    await self.send_message(bot, user_id, "El número es incorrecto o ya has intentado con él.")
            self.data_manager.save_info(self.users_data)

        else:
            await self.game_finished_message(bot, user_id)
