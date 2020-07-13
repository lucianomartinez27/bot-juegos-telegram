#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from bot_telegram import BotTelegram
from ahorcado.funciones import plantilla_ahorcado


class BotTelegramAhorcado(BotTelegram):
    def __init__(self, nombre, token):
        BotTelegram.__init__(self, nombre, token)
        self.lista_palabras = "escopeta mandarina vasija perro zanahoria manzana computadora".upper().split()
        self.datos_usuarios = {}

    def start(self, update, context):
        bot = context.bot
        usuario = update.message.chat_id
        nombre = update.message.chat.first_name
        self.enviar_mensaje(bot, usuario, "Hola {}, bienvenido. Ingresa /jugar para comenzar.".format(nombre))

    def jugar(self, update, context):
        usuario = update.message.chat_id
        bot = context.bot
        self.datos_usuarios[usuario] = {}
        palabra = self.datos_usuarios[usuario]['palabra'] = random.choice(self.lista_palabras)
        lista_errores = self.datos_usuarios[usuario]['errores'] = []
        lista_aciertos = self.datos_usuarios[usuario]['adivinadas'] = []
        self.enviar_mensaje(bot, usuario, "Ingrese una letra como mensaje para comenzar a jugar:")
        self.enviar_mensaje(bot, usuario, plantilla_ahorcado(lista_errores, lista_aciertos, palabra))

    def elegir_letra(self, update, context):
        letra = update.message.text.upper()
        bot = context.bot
        usuario = update.message.chat_id
        nombre = update.message.chat.first_name
        if not self.datos_usuarios.get(usuario, None):  # Comprueba si hay datos del usuario.
            self.enviar_mensaje(bot, usuario, "Hola {}, ingresa /jugar para comenzar.".format(nombre))
        else:
            if len(letra) > 1 or letra.isnumeric():
                self.enviar_mensaje(bot, usuario, "POR FAVOR, INGRESA UNA LETRA.")
            else:
                lista_errores = self.datos_usuarios[usuario]['errores']
                palabra = self.datos_usuarios[usuario]['palabra']
                lista_aciertos = self.datos_usuarios[usuario]['adivinadas']
                if letra in lista_aciertos or letra in lista_errores:
                    self.enviar_mensaje(bot, usuario, 'YA HAS ELEGIDO ESA LETRA.')
                elif letra in palabra:
                    lista_aciertos.append(letra)
                else:
                    lista_errores.append(letra)
                self.enviar_mensaje(bot, usuario, plantilla_ahorcado(lista_errores, lista_aciertos, palabra))
                if len(lista_errores) == 6:
                    del self.datos_usuarios[usuario]
                    self.enviar_mensaje(bot, usuario, "HAS PERIDO")
                    self.enviar_mensaje(bot, usuario, "LA PALABRA ERA: {}".format(palabra))
                    self.enviar_mensaje(bot, usuario, "Ingresa /jugar para comenzar de nuevo.".format(nombre))
                elif len(lista_aciertos) == len(set(palabra)):
                    del self.datos_usuarios[usuario]
                    self.enviar_mensaje(bot, usuario, "FELICITACIONES, HAS GANADO.")
                    self.enviar_mensaje(bot, usuario, "Ingresa /jugar para comenzar de nuevo.".format(nombre))

