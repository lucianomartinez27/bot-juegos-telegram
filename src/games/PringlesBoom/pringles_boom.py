import json
import random
from utils.errors import ModelError

class PringlesBoomGame:
    # Game phases
    PHASE_SETUP = "setup"
    PHASE_CHOOSING_EMOJI = "choosing_emoji"
    PHASE_PLAYING = "playing"
    PHASE_FINISHED = "finished"

    def __init__(self, player1_id=None, player2_id=None, player1_name=None, player2_name=None) -> None:
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.player1_name = player1_name or "Player 1"
        self.player2_name = player2_name or "Player 2"
        # Grid states: 0 = untouched, 1 = safe, 2 = bomb exploded
        self.grid1 = [0] * 9
        self.grid2 = [0] * 9
        # Bomb locations (indices 0-8)
        self.bombs1 = []
        self.bombs2 = []
        # Turn: 1 for Player 1, 2 for Player 2
        self.turn = 1
        self.exploded_count1 = 0
        self.exploded_count2 = 0
        self.game_finished = False
        self.winner_id = None
        self.phase = self.PHASE_SETUP
        self.player1_emoji = "🥔"
        self.player2_emoji = "🥔"

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        game = cls()
        for key, value in data.items():
            setattr(game, key, value)
        return game

    def finished(self):
        return self.game_finished

    def place_bomb(self, user_id, cell_index, grid_num, user_name=None):
        if self.phase == self.PHASE_CHOOSING_EMOJI:
            raise ModelError("You must choose an emoji first!")
        if self.phase != self.PHASE_SETUP:
            raise ModelError("You can't place bombs now!")

        # Initialize Player 1 if not set
        if self.player1_id is None:
            self.player1_id = user_id
            if user_name:
                self.player1_name = user_name
        
        # Determine if this user is already registered as a player
        if user_id == self.player1_id:
            if grid_num != 1:
                raise ModelError("You are Player 1! You can only place bombs on your own board.")
        elif self.player2_id == user_id:
            if grid_num != 2:
                raise ModelError("You are Player 2! You can only place bombs on your own board.")
        elif self.player2_id is None:
            # New user wants to be Player 2
            self.player2_id = user_id
            if user_name:
                self.player2_name = user_name
            if grid_num != 2:
                raise ModelError("You are Player 2! You can only place bombs on your own board.")
        else:
            # Someone else entirely
            raise ModelError("You are not part of this game.")

        if grid_num == 1:
            if cell_index in self.bombs1:
                self.bombs1.remove(cell_index)
            elif len(self.bombs1) < 3:
                self.bombs1.append(cell_index)
            else:
                raise ModelError("You can only place 3 bombs!")
        elif grid_num == 2:
            if cell_index in self.bombs2:
                self.bombs2.remove(cell_index)
            elif len(self.bombs2) < 3:
                self.bombs2.append(cell_index)
            else:
                raise ModelError("You can only place 3 bombs!")
        
        if len(self.bombs1) == 3 and len(self.bombs2) == 3:
            self.phase = self.PHASE_CHOOSING_EMOJI

    def set_emoji(self, user_id, emoji):
        if self.phase != self.PHASE_CHOOSING_EMOJI:
            raise ModelError("You can't choose an emoji now!")
        
        if user_id == self.player1_id:
            self.player1_emoji = emoji
        elif user_id == self.player2_id:
            self.player2_emoji = emoji
        else:
            raise ModelError("You are not part of this game.")

        if self.player1_emoji != "🥔" and self.player2_emoji != "🥔":
            self.phase = self.PHASE_PLAYING
            self.turn = 1

    def pick(self, user_id, cell_index, grid_num, user_name=None):
        if self.phase == self.PHASE_SETUP:
            self.place_bomb(user_id, cell_index, grid_num, user_name=user_name)
            return self.game_finished

        if self.game_finished:
            raise ModelError("The game has already finished.")
        
        # Verify it's the player's turn
        if self.turn == 1:
            if user_id != self.player1_id:
                if user_id == self.player2_id:
                    raise ModelError("Wait your turn! ✋")
                else:
                    raise ModelError("You are not part of this game.")
            
            # Player 1 must pick from Player 2's grid (grid_num == 2)
            if grid_num != 2:
                raise ModelError("You must pick from your opponent's grid!")

            if self.grid2[cell_index] != 0:
                raise ModelError("This chip has already been picked.")
            
            if cell_index in self.bombs2:
                self.grid2[cell_index] = 2
                self.exploded_count2 += 1
                if self.exploded_count2 >= 3:
                    self.game_finished = True
                    self.phase = self.PHASE_FINISHED
                    self.winner_id = self.player1_id
            else:
                self.grid2[cell_index] = 1
            
            self.turn = 2
        else:
            if user_id != self.player2_id:
                if user_id == self.player1_id:
                    raise ModelError("Wait your turn! ✋")
                else:
                    # Someone else trying to play?
                    raise ModelError("You are not part of this game.")
            
            # Player 2 must pick from Player 1's grid (grid_num == 1)
            if grid_num != 1:
                raise ModelError("You must pick from your opponent's grid!")

            if self.grid1[cell_index] != 0:
                raise ModelError("This chip has already been picked.")
            
            if cell_index in self.bombs1:
                self.grid1[cell_index] = 2
                self.exploded_count1 += 1
                if self.exploded_count1 >= 3:
                    self.game_finished = True
                    self.phase = self.PHASE_FINISHED
                    self.winner_id = self.player2_id
            else:
                self.grid1[cell_index] = 1
            
            self.turn = 1
        
        return self.game_finished

    def get_grid(self, player_num):
        return self.grid1 if player_num == 1 else self.grid2

    def get_bombs(self, player_num):
        return self.bombs1 if player_num == 1 else self.bombs2
