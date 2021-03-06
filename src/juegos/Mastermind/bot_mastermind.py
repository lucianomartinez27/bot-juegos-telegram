#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Juego : MUERTOS Y HERIDOS - MASTERMIND
"""

from src.bot_base import BotBase
from src.juegos.Mastermind.funciones import generar_numero, comprobar_numero \
, chequear_numero, partida_ganada, partida_perdida
import os

class BotMastermind(BotBase):
    def __init__(self):
        super(BotMastermind, self).__init__(os.path.abspath('juegos/'+self.nombre()))

    def nombre(self):
        return 'Mastermind'

    def generar_datos(self, id_usuario):
        # id_usuario se convierte en string porque las claves json deben ser de ese tipo
        self.datos_usuarios[str(id_usuario)] = {}
        self.datos_usuarios[str(id_usuario)]['numeros_computadora'] = generar_numero()
        self.datos_usuarios[str(id_usuario)]['lista_resultados'] = []
        self.datos_usuarios[str(id_usuario)]['lista_intentos'] = []
        self.datos_usuarios[str(id_usuario)]['partida_terminada'] = False
        self.data_manager.save_info(self.datos_usuarios)

    def jugar(self, update, context):
        id_usuario = update.callback_query.message.chat_id
        bot = context.bot
        self.generar_datos(id_usuario)
        self.enviar_mensaje(bot, id_usuario, 'MUERTOS Y HERIDOS (MASTERMIND)')
        self.enviar_mensaje(bot, id_usuario,
                            'Adivina un número de 4 dígitos, si aciertas el número, pero no la posición\n'
                            'tienes un herido. Si aciertas el número y su posición tienes un muerto.')
        self.enviar_mensaje(bot, id_usuario, 'Para ganar necesitas conseguir 4 muertos. Tendrás 15 intentos.')

    def responder_mensaje(self, update, context):
        mensaje = update.message.text
        bot = context.bot
        id_usuario = update.message.chat_id
        nombre = update.message.chat.first_name

        numeros_computadora = self.datos_usuarios[str(id_usuario)]['numeros_computadora']
        lista_resultados = self.datos_usuarios[str(id_usuario)]['lista_resultados']
        lista_intentos = self.datos_usuarios[str(id_usuario)]['lista_intentos']

        if not self.datos_usuarios[str(id_usuario)]['partida_terminada']:
            if partida_ganada(mensaje, numeros_computadora):
                self.enviar_mensaje(bot, id_usuario, "Felicidades, {}, GANASTE!!\n ¿Quieres jugar de nuevo? (Si o No)"\
                                    .format(nombre))
                self.enviar_mensaje(bot, id_usuario, "Para cambiar de juego, usa /juegos.")
                self.datos_usuarios[str(id_usuario)]['partida_terminada'] = True
            elif partida_perdida(lista_intentos):
                self.enviar_mensaje(bot, id_usuario, "Lo siento, {}, PERDISTE!!\n El número era {}\n¿Quieres jugar de \
                                                   nuevo? (Si o No)".format(nombre, "".join(numeros_computadora)))
                self.enviar_mensaje(bot, id_usuario, "Para cambiar de juego, usa /juegos.")
                self.datos_usuarios[str(id_usuario)]['partida_terminada'] = True
            else:
                if comprobar_numero(mensaje, lista_intentos):
                    self.enviar_mensaje(bot, id_usuario,
                                        chequear_numero(numeros_computadora, mensaje, lista_intentos, lista_resultados))
                else:
                    self.enviar_mensaje(bot, usuario, "El número es incorrecto o ya has intentado con él.")
            self.data_manager.save_info(self.datos_usuarios)

        else:
            self.enviar_mensaje(bot, id_usuario, "El juego ya terminó. Utiliza /juegos para comenzar uno nuevo.")
