#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Librerias telegram
from telegram.ext import ApplicationBuilder, Updater, MessageHandler, CommandHandler,\
                         filters, CallbackQueryHandler, ConversationHandler,\
                         InlineQueryHandler

# Registro de actividades
import logging


class BotTelegram:
    """Clase base para crear instancias de un Bot de Telegram

        >>> MiBot = BotTelegram(nombre, token)

    """

    def __init__(self, nombre, token):
        """Inicializa las variables básicas para que el bot de Telegram funcione."""
        # loggin: Sirve para enviar un registro de las actividades.
        self.app = ApplicationBuilder().token(token).build()
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger(nombre)
        # Polling se pone a la espera de que se ingresen comandos
        # Dispatcher: está al pendiente de todas las ventanas donde se encuentra el bot.
    def run(self):
        self.app.run_polling()

    async def enviar_mensaje(self, bot, id_usuario, mensaje, parse_mode=None) -> object:
        """Función que envía un mensaje desde un bot y a un usuario en particular.
        Parámetros:
            bot: objeto Bot de el módulo telegram.
                Tipo: telegram.bot
            usuario: id de telegram del usuario.
                Tipo: (int)
            text: mensaje a enviar.
                Tipo: (str)
            parse_mode: establece como se 'parsea' el texto enviado.
                Tipo: (str)
                Ejm: 'Markdown'; 'HTML'.
            """
        await bot.send_message(chat_id=id_usuario, text=mensaje, parse_mode=parse_mode)

    def esperar_comando(self, comando, funcion):
        """
        Función que espera que se ingrese en el chat el comando y ejecuta la función que se ingresen como parámetro.
        Parámetros:
            comando: texto que colocará el usuario acompañado de una barra '/' en el chat de Telegram..
                Tipo: (str)
                Ejemplo: 'start'
            funcion: función que se ejecutará cuando el usuario realice determinado comando.
                Tipo: (fn)
        """
        self.app.add_handler(CommandHandler(comando, funcion))
          
    def contestar_consulta(self, funcion, patron=None):
        """Función que espera que el usuario presione un botón que se despliega en el chat de telegram y ejecuta la
        función que se pase como parámetro.
        Parametro:
            funcion: función que se ejecuta al presionar un botón (InlineKeyboardButton) en el chat.
                Tipo: (fn)"""
        self.app.add_handler(CallbackQueryHandler(funcion, pattern=patron))

    def contestar_consulta_por_estado(self, funcion, estados):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', funcion)],
            states=estados,
            fallbacks=[CommandHandler('start', funcion)]
        )

        self.app.add_handler(conv_handler)
    
    def contestar_mensaje(self, funcion):
        """ Espera cualquier cosa en el chat que no sea un comando (mensajes) y ejecuta la función que se pase como
            parámetro.
        Parametro:
        funcion: función que se ejecuta al recibir un mensaje en el chat.
            Tipo:: (fn)"""
        mensaje_recibido = MessageHandler(filters.TEXT & (~filters.COMMAND), funcion)
        self.app.add_handler(mensaje_recibido)

    def contestar_inlinemode(self, comando, patron=None):
        self.app.add_handler(InlineQueryHandler(comando, pattern=patron))

    def generar_id_usuario(self, update):
        try:
            id = update.callback_query.message.chat_id
        except:
            try:
                id = update.message.chat_id
            except:
                try:
                    id = update.inline_query.from_user.id
                except:
                    id = update.callback_query.from_user.id
        return id

    def generar_id_mensaje(self, update):
        try:
            id = update.callback_query.message.message_id
        except:
            try:
                id = update.message.message_id
            except:
                try:
                    id = update.inline_query.from_user.message_id
                except:
                    id = update.callback_query.inline_message_id
        return id