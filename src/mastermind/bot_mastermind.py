#!/usr/bin/env python3
#-*- coding: utf-8 -*-

"""
Juego : MUERTOS Y HERIDOS - MASTERMIND
"""

import random
from mastermind.funciones import generar_numero, comprobar_numero, chequear_numero, contar_muertos_y_heridos
from bot_telegram import BotTelegram
import json

class BotMastermind(BotTelegram):
    def __init__(self):
        self.datos_usuarios = {}
        try:
            with open('src/mastermind/data.json', 'r+') as datafile:
                self.datos_usuarios = json.load(datafile)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open('src/mastermind/data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))

    def jugar(self, update, context):
        if update.callback_query:
             id_usuario = update.callback_query.message.chat_id
        else:
            id_usuario = update.message.chat_id
        bot = context.bot

        # id_usuario se convierte en string porque las claves json deben ser de ese tipo
        self.datos_usuarios[str(id_usuario)] = {}
        self.datos_usuarios[str(id_usuario)]['numeros_computadora'] = generar_numero()
        self.datos_usuarios[str(id_usuario)]['lista_resultados'] = []
        self.datos_usuarios[str(id_usuario)]['lista_intentos'] = []
        self.datos_usuarios[str(id_usuario)]['gano_o_perdio'] = False
        with open('src/mastermind/data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))

        self.enviar_mensaje(bot, id_usuario, 'MUERTOS Y HERIDOS (MASTERMIND)')
        self.enviar_mensaje(bot, id_usuario, 'Adivina un número de 4 dígitos, si aciertas el número, pero no la posición\ntienes un herido. Si aciertas el número y su posición tienes un muerto.')
        self.enviar_mensaje(bot, id_usuario, 'Para ganar necesitas conseguir 4 muertos. Tendrás 15 intentos.')
    

    n_computadora = generar_numero()
    # Bucle principal
    def responder_mensaje(self, update, context):
        mensaje = update.message.text
        bot = context.bot
        usuario = update.message.chat_id
        nombre = update.message.chat.first_name

        numeros_computadora = self.datos_usuarios[str(usuario)]['numeros_computadora']
        lista_resultados = self.datos_usuarios[str(usuario)]['lista_resultados']
        lista_intentos = self.datos_usuarios[str(usuario)]['lista_intentos']
        
        if not self.datos_usuarios[str(usuario)]['gano_o_perdio']:
            if contar_muertos_y_heridos(mensaje, numeros_computadora) == (4, 0):
                self.enviar_mensaje(bot, usuario, "FELICIDADES, GANASTE!!\n ¿Quieres jugar de nuevo? (Si o No)")
                self.enviar_mensaje(bot, usuario, "Para cambiar de juego, usa /juegos.")
                self.datos_usuarios[str(usuario)]['gano_o_perdio'] = True
            elif len(lista_intentos) >= 14:
                self.enviar_mensaje(bot, usuario, "LO SIENTO, PERDISTE!!\n El número era {}\n¿Quieres jugar de nuevo? (Si o No)".format("".join(numeros_computadora)))
                self.enviar_mensaje(bot, usuario, "Para cambiar de juego, usa /juegos.")
                self.datos_usuarios[str(usuario)]['gano_o_perdio'] = True
            else:
                if comprobar_numero(mensaje, lista_intentos):
                    self.enviar_mensaje(bot, usuario, chequear_numero(numeros_computadora, mensaje, lista_intentos, lista_resultados))
                else:
                    self.enviar_mensaje(bot, usuario, "El número es incorrecto o ya has intentado con él.")
            with open('src/mastermind/data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))

        else:
            if mensaje.upper().startswith('S'):
                self.jugar(update, context)
            elif mensaje.upper().startswith('N'):
                del self.datos_usuarios[str(usuario)]
                self.enviar_mensaje(bot, usuario, "Para jugar a otro juego puedes usar /juegos")
            else:
                self.enviar_mensaje(bot, usuario, "Por favor, ingresa sí o no.")
        
        
            
        
