import random

class Rock:
    name = 'rock'

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

    def play_against(self, oponent):
        return oponent.play_against_paper()
    
    def play_against_rock(self):
        return 'paper'
    
    def play_against_paper(self):
        return 'tie'
    
    def play_against_scissor(self):
        return 'scissor'

class Scissor:
    name = 'scissor'

    def play_against(self, oponent):
        return oponent.play_against_scissor()
    
    def play_against_rock(self):
        return 'rock'
    
    def play_against_paper(self):
        return 'scissor'

    def play_against_scissor(self):
        return 'tie'

class RockPaperScissorGame:
    def __init__(self, player_one, player_two) -> None:
        self.player_one = player_one
        self.player_two = player_two



    def play(self):
        return self.player_one.play_against(self.player_two)

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

    