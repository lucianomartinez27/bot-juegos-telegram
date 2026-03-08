import json
from .mastermind import MasterMind

class MultiplayerMasterMind(MasterMind):
    def __init__(self, num_digits: int = 4, max_attempts: int = 15) -> None:
        super().__init__(num_digits, max_attempts)
        self.creator_id = None
        self.combination_set = False
        # We start with empty numbers if it's multiplayer, they will be set by the creator
        self.numbers = []

    def set_combination(self, combination: list):
        if len(combination) != self.num_digits:
             return False
        self.numbers = combination
        self.combination_set = True
        return True

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        game = cls(num_digits=data.get('num_digits', 4), max_attempts=data.get('max_attempts', 15))
        game.numbers = data['numbers']
        game.attempts = data['attempts']
        game.results = data['results']
        game.game_finished = data['game_finished']
        game.current_guess = data.get('current_guess', "")
        game.creator_id = data.get('creator_id')
        game.combination_set = data.get('combination_set', False)
        return game
