#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import json
import random
from utils.errors import ModelError

class MasterMind:
	def __init__(self) -> None:
		self.numbers = self.generate_numbers()
		self.attempts = []
		self.results = []
		self.game_finished = False
	
	def to_json(self):
		return json.dumps(self.__dict__)
	
	@classmethod
	def from_json(cls, json_str):
			data = json.loads(json_str)
			game = cls()
			game.numbers = data['numbers']
			game.attempts = data['attempts']
			game.results = data['results']
			game.game_finished = data['game_finished']
			return game
	
	def finished(self):
		return self.game_finished

	def generate_numbers(self):
		""" Genera 4 números aleatorios, del 0 al 9, todos distintos."""
		numbers = []
		while len(numbers) < 4:
			number = str(random.randint(0, 9))
			if number not in numbers:
				numbers.append(number)
		return numbers

	def check_number(self, numbers_to_check):
		"""pide al usuario un número de cuatro cifras y comprueba que no estén en
			una lista donde se guardan intentos"""

		# TODO: Assert and throw error
		if len(numbers_to_check) != 4 or not numbers_to_check.isnumeric():
			raise ModelError('The number is invalid. It must have 4 digits')
		elif numbers_to_check in self.attempts:
			raise ModelError('You already tried this number')
		elif len(set(numbers_to_check)) != len(numbers_to_check): # Some repeated number
			raise ModelError('There must be no repeated numbers')

		self.attempts.append(numbers_to_check)
		self.results.append(self.count_exact_and_partial_matches(numbers_to_check))
		return numbers_to_check
		
	def count_exact_and_partial_matches(self, numbers_to_check):
		correct_number = 0
		currect_number_and_position = 0
		for position, number in enumerate(numbers_to_check):
			if number == self.numbers[position]:
				currect_number_and_position += 1
			elif number in self.numbers:
				correct_number += 1
			
		return currect_number_and_position, correct_number

	def is_winner(self):
		last_result = self.results[len(self.results) - 1]
		return last_result == (4, 0)

	def is_looser(self):
		return len(self.attempts) > 14

	def template(self):
		"""comprueba el número de muertos y heridos que obtuvo el usuario"""

		texto = "You have {} attempts left ".format(15-len(self.attempts))
		texto += '\nDEADS - INJURED'.center(30)

		for i in range(len(self.attempts)):
			exacts, partials = self.results[i][0], self.results[i][1]
			texto += '\n{}:    {}         {}'.format(self.attempts[i], exacts, partials)

		return texto