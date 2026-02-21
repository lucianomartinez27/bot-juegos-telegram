#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram_bot import BotTelegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, InlineQueryHandler, filters

class RedirectBot(BotTelegram):
    def __init__(self, name, token):
        super().__init__(name, token)

    async def send_redirect_message(self, update, context):
        """Send a message informing that the bot has moved."""
        message = (
            "🚀 **We have moved! / ¡Nos hemos mudado!**\n\n"
            "This bot is no longer active. To continue playing classic games, "
            "please visit our new bot: @the\_classic\_games\_bot\n\n"
            "Este bot ya no está activo. Para seguir jugando a los juegos clásicos, "
            "por favor visita nuestro nuevo bot: @the\_classic\_games\_bot"
        )
        
        keyboard = [
            [InlineKeyboardButton("Go to New Bot / Ir al nuevo Bot 🎮", url="https://t.me/the_classic_games_bot")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Handle message interaction
        if update.message:
            await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='markdown')
        # Handle button interaction (if any)
        elif update.callback_query:
            await update.callback_query.answer()
            await update.callback_query.message.reply_text(message, reply_markup=reply_markup, parse_mode='markdown')
        # Handle inline query
        elif update.inline_query:
            await update.inline_query.answer([], switch_pm_text="We moved! / ¡Nos mudamos!", switch_pm_parameter="redirect")

    def setup(self):
        """Set up all handlers to point to the redirect message."""
        # Use generic handlers for everything
        self.app.add_handler(MessageHandler(filters.COMMAND, self.send_redirect_message)) # Handle all commands
        self.app.add_handler(MessageHandler(filters.ALL & (~filters.COMMAND), self.send_redirect_message))
        self.app.add_handler(CallbackQueryHandler(self.send_redirect_message))
        self.app.add_handler(InlineQueryHandler(self.send_redirect_message))


#!/usr/bin/env python3
# -*- coding: utf-8 -*-




if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()

    TOKEN_TELEGRAM_REDIRECT = os.getenv('TOKEN_TELEGRAM_REDIRECT')

    if not TOKEN_TELEGRAM_REDIRECT:
        print("Error: TOKEN_TELEGRAM_REDIRECT not found in .env file.")
        exit(1)

    print("Starting Redirect Bot...")
    redirect_bot = RedirectBot("Redirect Bot", TOKEN_TELEGRAM_REDIRECT)
    redirect_bot.setup()
    redirect_bot.run()
