import random

class Rock:
    name = 'piedra'

    def play_against(self, oponent):
        return oponent.play_against_rock()
    
    def play_against_rock(self):
        return 'empate'
    
    def play_against_paper(self):
        return 'papel'
    
    def play_against_scissor(self):
        return 'piedra'
    

class Paper:
    name = 'papel'

    def play_against(self, oponent):
        return oponent.play_against_paper()
    
    def play_against_rock(self):
        return 'papel'
    
    def play_against_paper(self):
        return 'empate'
    
    def play_against_scissor(self):
        return 'tijera'

class Scissor:
    name = 'tijera'

    def play_against(self, oponent):
        return oponent.play_against_scissor()
    
    def play_against_rock(self):
        return 'piedra'
    
    def play_against_paper(self):
        return 'tijera'

    def play_against_scissor(self):
        return 'empate'

class RockPaperScissorGame:
    def __init__(self, player_one, player_two) -> None:
        self.player_one = player_one
        self.player_two = player_two

    def play(self):
        return self.player_one.play_against(self.player_two)
    
    def player_one_choice(self):
        return self.player_one.name
    
    def player_two_choice(self):
        return self.player_two.name
    
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

    