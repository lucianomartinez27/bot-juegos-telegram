#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram_bot import BotTelegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, InlineQueryHandler, filters

class RedirectBot(BotTelegram):
    def __init__(self, name, token, new_bot_username="PlayTheGamesBot"):
        super().__init__(name, token)
        self.new_bot_username = new_bot_username
        self.new_bot_url = f"https://t.me/{new_bot_username}"

    async def send_redirect_message(self, update, context):
        """Send a message informing that the bot has moved."""
        escaped_username = self.new_bot_username.replace('_', r'\_')
        message = (
            "🚀 **We have moved! / ¡Nos hemos mudado!**\n\n"
            "This bot is no longer active. To continue playing classic games, "
            f"please visit our new bot: @{escaped_username}\n\n"
            "Este bot ya no está activo. Para seguir jugando a los juegos clásicos, "
            f"por favor visita nuestro nuevo bot: @{escaped_username}"
        )
        
        keyboard = [
            [InlineKeyboardButton("Go to New Bot / Ir al nuevo Bot 🎮", url=self.new_bot_url)]
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
    NEW_BOT_USERNAME = os.getenv('BOT_USERNAME', 'PlayTheGamesBot')
    redirect_bot = RedirectBot("Redirect Bot", TOKEN_TELEGRAM_REDIRECT, NEW_BOT_USERNAME)
    redirect_bot.setup()
    redirect_bot.run()
