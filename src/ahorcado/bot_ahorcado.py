#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import json
from bot_telegram import BotTelegram
from .funciones import plantilla_ahorcado, letra_valida


class BotTelegramAhorcado(BotTelegram):
    def __init__(self):
        self.lista_palabras = "escopeta mandarina vasija perro zanahoria manzana computadora".upper().split()
        self.datos_usuarios = {}
        try:
            with open('ahorcado/data.json', 'r+') as datafile:
                self.datos_usuarios = json.load(datafile)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open('ahorcado/data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))
    def generar_datos(self, id_usuario):
        # id_usuario se convierte en string porque las claves json deben ser de ese tipo
        self.datos_usuarios[str(id_usuario)] = {}
        self.datos_usuarios[str(id_usuario)]['palabra'] = random.choice(self.lista_palabras)
        self.datos_usuarios[str(id_usuario)]['errores'] = []
        self.datos_usuarios[str(id_usuario)]['adivinadas'] = []
        self.datos_usuarios[str(id_usuario)]['partida_terminada'] = False
        with open('ahorcado/data.json', 'w') as datafile:
            datafile.write(json.dumps(self.datos_usuarios))

    def jugar(self, update, context):
        id_usuario = update.callback_query.message.chat_id
        bot = context.bot
        self.generar_datos(id_usuario)
        palabra = self.datos_usuarios[str(id_usuario)]['palabra']
        self.enviar_mensaje(bot, id_usuario, "Ingrese una letra como mensaje para jugar:")
        self.enviar_mensaje(bot, id_usuario, plantilla_ahorcado([], [], palabra))

    def responder_mensaje(self, update, context):
        letra = update.message.text.upper()
        bot = context.bot
        usuario = update.message.chat_id
        nombre = update.message.chat.first_name
        lista_errores = self.datos_usuarios[str(usuario)]['errores']
        palabra = self.datos_usuarios[str(usuario)]['palabra']
        lista_aciertos = self.datos_usuarios[str(usuario)]['adivinadas']

        if not self.datos_usuarios[str(usuario)]['partida_terminada']:
            if not letra_valida(letra):
                self.enviar_mensaje(bot, usuario, "POR FAVOR, INGRESA UNA LETRA.")
            elif letra in lista_aciertos or letra in lista_errores:
                self.enviar_mensaje(bot, usuario, 'YA HAS ELEGIDO ESA LETRA.')
            elif letra in palabra:
                lista_aciertos.append(letra)
            else:
                lista_errores.append(letra)
            self.enviar_mensaje(bot, usuario, plantilla_ahorcado(lista_errores, lista_aciertos, palabra))
            if len(lista_errores) == 6:
                del self.datos_usuarios[str(usuario)]
                self.enviar_mensaje(bot, usuario, "HAS PERIDO\nA PALABRA ERA: {}".format(palabra))
                self.enviar_mensaje(bot, usuario, "{}, ¿quieres jugar de nuevo? (Si o No)".format(nombre))
                self.datos_usuarios[str(usuario)]['partida_terminada'] = True
            elif len(lista_aciertos) == len(set(palabra)):
                self.enviar_mensaje(bot, usuario, "FELICITACIONES, HAS GANADO.")
                self.enviar_mensaje(bot, usuario, "¿{}, quieres jugar de nuevo? (Si o No)".format(nombre))
                self.datos_usuarios[str(usuario)]['partida_terminada'] = True
            with open('ahorcado/data.json', 'w') as datafile:
                datafile.write(json.dumps(self.datos_usuarios))
        else:
            if letra.upper().startswith('S'):
                self.jugar(update, context)
            elif letra.upper().startswith('N'):
                self.enviar_mensaje(bot, usuario, "Para jugar a otro juego puedes usar /juegos")
            else:
                self.enviar_mensaje(bot, usuario, "Por favor, ingresa sí o no.")
