#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import json
import random
from utils.errors import ModelError

class MasterMind:
    def __init__(self, num_digits: int = 4, max_attempts: int = 15) -> None:
        self.num_digits = num_digits
        self.max_attempts = max_attempts
        self.numbers = self.generate_numbers()
        self.attempts = []
        self.results = []
        self.game_finished = False
        self.current_guess = ""

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
        return game

    def finished(self):
        return self.game_finished

    def generate_numbers(self):
        """ Genera num_digits números aleatorios, del 0 al 6, todos distintos."""
        numbers = []
        while len(numbers) < self.num_digits:
            number = str(random.randint(0, 6))
            if number not in numbers:
                numbers.append(number)
        return numbers

    def check_number(self, numbers_to_check):
        """pide al usuario un número de num_digits cifras y comprueba que no estén en
            una lista donde se guardan intentos"""

        # TODO: Assert and throw error
        if len(numbers_to_check) != self.num_digits:
            raise ModelError('The combination is invalid. It must have {} elements'.format(self.num_digits))
        elif numbers_to_check in self.attempts:
            raise ModelError('You already tried this combination')
        elif len(set(numbers_to_check)) != len(numbers_to_check): # Some repeated number
            raise ModelError('There must be no repeated elements')

        self.attempts.append(numbers_to_check)
        self.results.append(self.count_exact_and_partial_matches(numbers_to_check))
        return numbers_to_check

    def count_exact_and_partial_matches(self, numbers_to_check):
        results = []
        for position, number in enumerate(numbers_to_check):
            if number == self.numbers[position]:
                results.append(1) # Exact match
            elif number in self.numbers:
                results.append(2) # Partial match
            else:
                results.append(3) # No match

        return results

    def is_winner(self):
        last_result = self.results[len(self.results) - 1]
        return all(r == 1 for r in last_result)

    def is_looser(self):
        return len(self.attempts) >= self.max_attempts

    def template(self, attempts_left_label: str = "You have {} attempts left ", status_label: str = "Results", formatter: callable = None):
        """comprueba el número de muertos y heridos que obtuvo el usuario"""

        texto = attempts_left_label.format(self.max_attempts - len(self.attempts))
        texto += '\n' + status_label.center(30)

        for i in range(len(self.attempts)):
            result = self.results[i]
            attempt_display = self.attempts[i]
            if formatter:
                attempt_display = formatter(attempt_display)
            color_map = {1: "⚫", 2: "⚪", 3: "❌"}
            status_display = "".join([color_map[r] for r in result])
            texto += f'\n{attempt_display}: {status_display}'

        return texto