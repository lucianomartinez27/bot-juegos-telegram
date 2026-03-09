import json
from utils.errors import ModelError
import random
from internationalization import _

class Connect4Game:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[" " for _ in range(cols)] for _ in range(rows)]
        self.game_finished = False
        self.last_movement_symbol = ''
        self.winner = None

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        game = cls(data['rows'], data['cols'])
        game.board = data['board']
        game.game_finished = data['game_finished']
        game.last_movement_symbol = data['last_movement_symbol']
        game.winner = data.get('winner')
        return game

    def get_players_symbols(self, player_symbol):
        if player_symbol.upper() == 'R':
            self.player_symbol = '🔴'
            self.computer_symbol = '🟡'
        elif player_symbol.upper() == 'Y':
            self.player_symbol = '🟡'
            self.computer_symbol = '🔴'
        else:
            # For simplicity, default to Red/Yellow emojis if not R/Y
            self.player_symbol = '🔴'
            self.computer_symbol = '🟡'

    def is_winner(self, symbol):
        # Check horizontal
        for r in range(self.rows):
            for c in range(self.cols - 3):
                if self.board[r][c] == symbol and self.board[r][c+1] == symbol and \
                   self.board[r][c+2] == symbol and self.board[r][c+3] == symbol:
                    return True
        # Check vertical
        for r in range(self.rows - 3):
            for c in range(self.cols):
                if self.board[r][c] == symbol and self.board[r+1][c] == symbol and \
                   self.board[r+2][c] == symbol and self.board[r+3][c] == symbol:
                    return True
        # Check diagonal (positive slope)
        for r in range(3, self.rows):
            for c in range(self.cols - 3):
                if self.board[r][c] == symbol and self.board[r-1][c+1] == symbol and \
                   self.board[r-2][c+2] == symbol and self.board[r-3][c+3] == symbol:
                    return True
        # Check diagonal (negative slope)
        for r in range(self.rows - 3):
            for c in range(self.cols - 3):
                if self.board[r][c] == symbol and self.board[r+1][c+1] == symbol and \
                   self.board[r+2][c+2] == symbol and self.board[r+3][c+3] == symbol:
                    return True
        return False

    def is_full_board(self):
        for c in range(self.cols):
            if self.board[0][c] == " ":
                return False
        return True

    def mark_column(self, symbol, col):
        if col < 0 or col >= self.cols:
            raise ModelError(_("Columna inválida."))
        if self.board[0][col] != " ":
            raise ModelError(_("Esa columna ya está llena, por favor elige otra."))
        if self.last_movement_symbol == symbol:
            raise ModelError(_("Debes esperar a que tu oponente marque una casilla."))

        # Find the lowest empty row in this column
        for r in range(self.rows - 1, -1, -1):
            if self.board[r][col] == " ":
                self.board[r][col] = symbol
                break
        
        self.last_movement_symbol = symbol
        if self.is_winner(symbol):
            self.game_finished = True
            self.winner = symbol
        elif self.is_full_board():
            self.game_finished = True

    def finished(self):
        return self.game_finished

    def no_movement_done(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != " ":
                    return False
        return True

    def just_one_movement_done(self):
        count = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != " ":
                    count += 1
        return count == 1

class AgainstComputerConnect4(Connect4Game):
    def __init__(self, player_symbol='🔴', computer_symbol='🟡'):
        super().__init__()
        self.player_symbol = player_symbol
        self.computer_symbol = computer_symbol

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        game = cls(data.get('player_symbol', '🔴'), data.get('computer_symbol', '🟡'))
        game.board = data['board']
        game.game_finished = data['game_finished']
        game.last_movement_symbol = data['last_movement_symbol']
        game.winner = data.get('winner')
        return game

    def started(self):
        return self.last_movement_symbol != '' or not self.no_movement_done()

    def make_computer_movement(self):
        if self.game_finished:
            return

        # Simple AI: 
        # 1. Win if possible
        # 2. Block player if they can win
        # 3. Random move
        
        valid_cols = [c for c in range(self.cols) if self.board[0][c] == " "]
        if not valid_cols:
            return

        # 1. Win if possible
        for c in valid_cols:
            copy_game = Connect4Game.from_json(self.to_json())
            copy_game.last_movement_symbol = self.player_symbol # allow computer to move
            copy_game.mark_column(self.computer_symbol, c)
            if copy_game.is_winner(self.computer_symbol):
                self.mark_column(self.computer_symbol, c)
                return

        # 2. Block player
        for c in valid_cols:
            copy_game = Connect4Game.from_json(self.to_json())
            copy_game.last_movement_symbol = self.computer_symbol # allow player to move
            copy_game.mark_column(self.player_symbol, c)
            if copy_game.is_winner(self.player_symbol):
                self.mark_column(self.computer_symbol, c)
                return

        # 3. Random
        self.mark_column(self.computer_symbol, random.choice(valid_cols))
