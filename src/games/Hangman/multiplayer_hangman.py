import json
from .hangman import HangManGame

class MultiPlayerHangManGame(HangManGame):
    def __init__(self, word: str) -> None:
        super().__init__(word)
        self.last_player_id = None

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        game = cls(data['_word'])
        game.errors = data['errors']
        game.guessed = data['guessed']
        game.game_finished = data['game_finished']
        game.last_player_id = data.get('last_player_id')
        return game
