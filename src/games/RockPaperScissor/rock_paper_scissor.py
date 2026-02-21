import random

class Rock:
    name = 'rock'
    
    def is_unchosen(self):
        return False

    def play_against(self, oponent):
        return oponent.play_against_rock()
    
    def play_against_rock(self):
        return 'tie'
    
    def play_against_paper(self):
        return 'paper'
    
    def play_against_scissor(self):
        return 'rock'
    

class Paper:
    name = 'paper'
    
    def is_unchosen(self):
        return False

    def play_against(self, oponent):
        return oponent.play_against_paper()
    
    def play_against_rock(self):
        return 'paper'
    
    def play_against_paper(self):
        return 'tie'
    
    def play_against_scissor(self):
        return 'scissors'

class Scissor:
    name = 'scissors'
    
    def is_unchosen(self):
        return False

    def play_against(self, oponent):
        return oponent.play_against_scissor()
    
    def play_against_rock(self):
        return 'rock'
    
    def play_against_paper(self):
        return 'scissors'

    def play_against_scissor(self):
        return 'tie'

class NoElement:
    
    def is_unchosen(self):
        return True

class RockPaperScissorGame:
    def __init__(self, player_one=NoElement(), player_two=NoElement()) -> None:
        self.player_one = player_one
        self.player_two = player_two
        self.last_winner = None

    def to_json(self):
        return {}
    
    @classmethod
    def from_json(cls, json):
        return cls()

    def play(self):
        self.last_winner = self.player_one.play_against(self.player_two)
        return self.last_winner
    
    def player_one_choice(self):
        return self.player_one.name
    
    def player_two_choice(self):
        return self.player_two.name
    
    def last_winner_is(self, a_player):
        return self.last_winner == a_player.name
    
    def last_winner_is_player_one(self):
        return self.last_winner_is(self.player_one)
    
    def no_player_choose(self):
        return self.player_one.is_unchosen() and self.player_two.is_unchosen()
    
    def one_player_choose(self):
        return self.player_one.is_unchosen() and not self.player_two.is_unchosen() \
        or self.player_two.is_unchosen() and not self.player_one.is_unchosen()
    
    def both_players_choose(self):
        return not self.player_one.is_unchosen() and not self.player_two.is_unchosen()
    @staticmethod
    def element(name):
        if Rock.name == name:
            return Rock()
        if Scissor.name == name:
            return Scissor()
        if Paper.name == name:
            return Paper()
        
    @staticmethod
    def random_choice():
        return random.choice([Rock(), Paper(), Scissor()])

    