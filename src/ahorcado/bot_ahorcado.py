#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import json
from bot_telegram import BotTelegram
from .funciones import plantilla_ahorcado


class BotTelegramAhorcado(BotTelegram):
    def __init__(self):
        self.lista_palabras = "escopeta mandarina vasija perro zanahoria manzana computadora".upper().split()
        self.datos_usuarios = {}
        try:
            with open('src/ahorcado/data.json', 'r+') as datafile:
                self.datos_usuarios = json.load(datafile)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open('src/ahorcado/data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))

    def jugar(self, update, context):
        if update.callback_query:
             id_usuario = update.callback_query.message.chat_id
        else:
            id_usuario = update.message.chat_id
        bot = context.bot
        # id_usuario se convierte en string porque las claves json deben ser de ese tipo
        self.datos_usuarios[str(id_usuario)] = {}
        palabra = self.datos_usuarios[str(id_usuario)]['palabra'] = random.choice(self.lista_palabras)
        lista_errores = self.datos_usuarios[str(id_usuario)]['errores'] = []
        lista_aciertos = self.datos_usuarios[str(id_usuario)]['adivinadas'] = []
        self.datos_usuarios[str(id_usuario)]['gano_o_perdio'] = False 
        with open('src/ahorcado/data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))
        self.enviar_mensaje(bot, id_usuario, "Ingrese una letra como mensaje para jugar:")
        self.enviar_mensaje(bot, id_usuario, plantilla_ahorcado(lista_errores, lista_aciertos, palabra))

    def responder_mensaje(self, update, context):
        letra = update.message.text.upper()
        bot = context.bot
        usuario = update.message.chat_id
        nombre = update.message.chat.first_name
        lista_errores = self.datos_usuarios[str(usuario)]['errores']
        palabra = self.datos_usuarios[str(usuario)]['palabra']
        lista_aciertos = self.datos_usuarios[str(usuario)]['adivinadas']

        if not self.datos_usuarios[str(usuario)]['gano_o_perdio']:
            if len(letra) > 1 or not letra.isalpha():
                self.enviar_mensaje(bot, usuario, "POR FAVOR, INGRESA UNA LETRA.")
            else:
                if letra in lista_aciertos or letra in lista_errores:
                    self.enviar_mensaje(bot, usuario, 'YA HAS ELEGIDO ESA LETRA.')
                elif letra in palabra:
                    lista_aciertos.append(letra)
                else:
                    lista_errores.append(letra)
                self.enviar_mensaje(bot, usuario, plantilla_ahorcado(lista_errores, lista_aciertos, palabra))
                if len(lista_errores) == 6:
                    del self.datos_usuarios[str(usuario)]
                    self.enviar_mensaje(bot, usuario, "HAS PERIDO")
                    self.enviar_mensaje(bot, usuario, "LA PALABRA ERA: {}".format(palabra))
                    self.enviar_mensaje(bot, usuario, "¿Quieres jugar de nuevo? (Si o No)")
                    self.datos_usuarios[str(usuario)]['gano_o_perdio'] = True
                elif len(lista_aciertos) == len(set(palabra)):
                    self.enviar_mensaje(bot, usuario, "FELICITACIONES, HAS GANADO.")
                    self.enviar_mensaje(bot, usuario, "¿Quieres jugar de nuevo? (Si o No)")
                    self.datos_usuarios[str(usuario)]['gano_o_perdio'] = True
            with open('src/ahorcado/data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))
        else:
            if letra.upper().startswith('S'):
                self.jugar(update, context)
            elif letra.upper().startswith('N'):
                self.enviar_mensaje(bot, usuario, "Para jugar a otro juego puedes usar /juegos")
            else:
                self.enviar_mensaje(bot, usuario, "Por favor, ingresa sí o no.")


