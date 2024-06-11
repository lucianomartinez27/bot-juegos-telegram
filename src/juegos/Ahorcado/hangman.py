import random
from utils.errors import ModelError

class HangManGame:
	def __init__(self) -> None:
		self.words = "escopeta mandarina vasija perro zanahoria manzana computadora".upper().split()
		self._word = random.choice(self.words)
		self.errors = []
		self.guessed = []
		self.game_finished = False

	def template(self) -> str:
		person = ("O", "|", "/", "\\", "/ '", "\\")
		gallow = ["  ", "  ", "  ", "  ", "  ", "  "]

		for i in range(len(self.errors)):
				gallow[i] = person[i]

		gallow_template = "*-------*\n"
		gallow_template += "||      |    \n"
		gallow_template += "||     {0}    \n".format(gallow[0])
		gallow_template += "||   {1} {0} {2}  \n".format(gallow[1], gallow[2], gallow[3])
		gallow_template += "||   {0} {1}   \n".format(gallow[4], gallow[5])
		gallow_template += "||           \n"
		gallow_template += "||=========\n\n"

		gallow_template += "palabra:"
		for letter in self._word:
				if letter not in self.guessed:
						gallow_template += " _"
				else:
						gallow_template += letter
		return gallow_template


	def is_valid_letter(self, letter: str) -> bool:
			return letter.isalpha() and len(letter) == 1

	def is_finished(self):
		return self.game_finished
	
	def letter_has_been_tried(self, letter):
		return letter in self.guessed or letter in self.errors

	def try_letter(self, letter):
		
		if not self.is_valid_letter(letter):
				raise ModelError("Por favor, escribe una sola letra.")
		
		if self.letter_has_been_tried(letter):
				raise ModelError("Ya has elegido esa letra.")

		if letter in self._word:
			self.guessed.append(letter)
		else:
			self.errors.append(letter)

		if (self.lost() or self.won()):
			self.game_finished = True
	
	def lost(self):
		return len(self.errors) == 6
	
	def won(self):
		return len(self.guessed) == len(set(self._word))
	
	def word(self):
		return self._word