# Classic Games Telegram Bot

A Telegram bot that allows you to play several classic games directly in your chat or with friends using inline mode.

## Try it out!
You can try the bot here: [Classic Games Bot](https://t.me/the_classic_games_bot)

## Features
- **Multi-language Support**: Users can choose between English 🇬🇧 and Spanish 🇪🇸 using the `/language` command.
- **Single Player Games**: Play against the bot in your private chat.
- **Multiplayer Games**: Challenge your friends in any chat using Telegram's Inline Mode.
- **Persistent Progress**: The bot saves your game state and language preferences.

## Available Games

### Single Player (use `/games`)
- **- Hangman**: Guess the hidden word letter by letter.
- **- Mastermind**: A logic game where you must guess a 4-digit code.
- **- Minesweeper**: Clear the board without hitting any mines.
- **- Tic-Tac-Toe**: The classic 3x3 game against the computer.
- **- Rock, Paper, Scissors**: Play against the computer.

### Multiplayer (Inline Mode - type `@the_classic_games_bot play`)
- **Tic-Tac-Toe MultiPlayer**: Challenge a friend in any chat.
- **Rock, Paper, Scissors Multiplayer**: Play against a friend.

## Setup and Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/bot-juegos-telegram.git
    cd bot-juegos-telegram
    ```

2.  **Configuration**:
    - Create a `.env` file in the root directory based on `.env.example`.
    - Get a Telegram Bot Token from [BotFather](https://t.me/botfather).
    - Add your token to the `.env` file:
      ```
      TOKEN_TELEGRAM=YOUR_TOKEN_HERE
      ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Bot**:
    ```bash
    python src/main.py
    ```

## Technologies Used
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/): The main library for interacting with the Telegram API.
- [gettext](https://docs.python.org/3/library/gettext.html): Used for internationalization (i18n).
- [python-dotenv](https://github.com/theskumar/python-dotenv): For managing environment variables.

## Requirements
- Python 3.10+
- `python-telegram-bot`
- `python-dotenv`
