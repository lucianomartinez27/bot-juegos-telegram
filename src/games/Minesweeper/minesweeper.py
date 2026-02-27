#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import random
import copy

MINE_CODE = 9
HIDDEN_CELL = u"\U00002B1C"
UNICODE_SYMBOLS = {0: " ", 1: u"\U00000031", 2: u"\U00000032", 3: u"\U00000033", 4: u"\U00000034",
				   5: u"\U00000035",
				   6: u"\U00000036", 7: u"\U00000037", 8: u"\U00000038", MINE_CODE: u"\U0001F4A3"}


class Minesweeper:
	def __init__(self, num_of_rows=8, num_of_cols=8, num_of_bombs=8) -> None:
		self.num_of_bombs = num_of_bombs
		self.num_of_rows = num_of_rows
		self.num_of_cols = num_of_cols
		self.hidden_board = [[0 for column in range(num_of_cols)] for row in range (num_of_rows)]
		self.visible_board = self.create_visible_board()
		self.game_status = 'playing'
		self.place_bombs()

	def to_json(self):
		return json.dumps(self.__dict__)
	
	@classmethod
	def from_json(cls, json_str):
			data = json.loads(json_str)
			game = cls(data['num_of_rows'], data['num_of_cols'], data['num_of_bombs'])
			game.hidden_board = data['hidden_board']
			game.visible_board = data['visible_board']
			game.game_status = data['game_status']

			return game

	def board(self):
		return self.visible_board
	
	def finished(self):
		return self.game_status != 'playing'
	
	def mark_cell(self, row_number, column_number):
		self.show_board_hints(row_number, column_number)
		if self.is_bomb(row_number, column_number):
			self.reveal_board()
			self.game_status = 'lose'
		if self.no_cell_to_be_mark():
			self.reveal_board()
			self.game_status = 'win'
		

	def is_bomb(self, row_number, column_number):
		return self.hidden_board[row_number][column_number] == MINE_CODE
	
	def place_bombs(self):
		bombs_placed  = 0
		while bombs_placed < self.num_of_bombs:
			row_number = random.randrange(self.num_of_rows)
			col_number = random.randrange(self.num_of_cols)
			if self.hidden_board[row_number][col_number] != MINE_CODE:
				self.hidden_board[row_number][col_number] = MINE_CODE
				bombs_placed += 1
		self.place_hints()
	
	def place_hints(self):
		
		for row_number in range(self.num_of_rows):
			for col_number in range(self.num_of_cols):
				if self.hidden_board[row_number][col_number] == MINE_CODE:
					for row_sibling in range(max(0, row_number-1), min(self.num_of_rows, row_number+2)):
						for column_sibling in range(max(0, col_number-1), min(self.num_of_cols, col_number+2)):
							if self.hidden_board[row_sibling][column_sibling] != MINE_CODE:
								self.hidden_board[row_sibling][column_sibling] += 1


	def create_visible_board(self):
		visible_board = copy.deepcopy(self.hidden_board)
		for row_number in range(self.num_of_rows):
			for col_number in range(self.num_of_cols):
				visible_board[row_number][col_number] = HIDDEN_CELL
		return visible_board



	def show_board_hints(self, row_number, column_number):
		can_be_cleared = self.visible_board[row_number][column_number] == HIDDEN_CELL
		no_bombs_near_cell = self.hidden_board[row_number][column_number] == 0
		self.visible_board[row_number][column_number] = UNICODE_SYMBOLS[self.hidden_board[row_number][column_number]]
		if no_bombs_near_cell and can_be_cleared:
			for row_sibling in range(max(0, row_number-1), min(self.num_of_rows, row_number+2)):
				for column_sibling in range(max(0, column_number-1), min(self.num_of_cols, column_number+2)):
					if self.hidden_board[row_sibling][column_sibling] != MINE_CODE:
						self.show_board_hints(row_sibling, column_sibling)

	def no_cell_to_be_mark(self):
		num_of_cells = self.num_of_rows * self.num_of_cols
		for row_number in range(self.num_of_rows):
			for column_number in range(self.num_of_cols):
				if self.visible_board[row_number][column_number] != HIDDEN_CELL:
					num_of_cells -= 1
		return (num_of_cells - self.num_of_bombs) == 0
	
	def is_winner(self):
		return self.game_status == 'win'
	
	def reveal_board(self):
		for row_number in range(self.num_of_rows):
			for column_number in range(self.num_of_cols):
				self.reveal_cell(row_number, column_number)

	def reveal_cell(self, row_number, column_number):
		self.visible_board[row_number][column_number] = UNICODE_SYMBOLS[self.hidden_board[row_number][column_number]]