#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import copy

MINE_CODE = 9
HIDDEN_CELL = u"\U00002B1C"
UNICODE_SYMBOLS = {0: " ", 1: u"\U00000031", 2: u"\U00000032", 3: u"\U00000033", 4: u"\U00000034",
                   5: u"\U00000035",
                   6: u"\U00000036", 7: u"\U00000037", 8: u"\U00000038", MINE_CODE: u"\U0001F4A3"}


def create_board(number_of_rows, number_of_columns, total_bombs):
    
    bombs_placed = 0
    board = [[0 for column in range(number_of_columns)] for row in range (number_of_rows)]
    while bombs_placed < total_bombs:
        x = random.randrange(number_of_rows)
        y = random.randrange(number_of_columns)
        if board[x][y] != MINE_CODE:
            board[x][y] = MINE_CODE
            bombs_placed += 1
    return place_hints(board)

def tablero_visible_inicial(board):
    tablero2 = copy.deepcopy(board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            tablero2[i][j] = HIDDEN_CELL
    return tablero2

MINE = 9

def place_hints(board):
    rows = len(board)
    cols = len(board[0])
    
    for row_number in range(rows):
        for col_number in range(cols):
            if board[row_number][col_number] == MINE:
                for row_sibling in range(max(0, row_number-1), min(rows, row_number+2)):
                    for column_sibling in range(max(0, col_number-1), min(cols, col_number+2)):
                        if board[row_sibling][column_sibling] != MINE:
                            board[row_sibling][column_sibling] += 1

    return board

def show_board_hints(row_number, column_number, hidden_board, visible_board):
    rows = len(hidden_board)
    cols = len(hidden_board[0])
    can_be_cleared = visible_board[row_number][column_number] == HIDDEN_CELL
    visible_board[row_number][column_number] = UNICODE_SYMBOLS[hidden_board[row_number][column_number]]
    if hidden_board[row_number][column_number] == 0 and can_be_cleared:
        for row_sibling in range(max(0, row_number-1), min(rows, row_number+2)):
            for column_sibling in range(max(0, column_number-1), min(cols, column_number+2)):
                if hidden_board[row_sibling][column_sibling] != MINE_CODE:
                    show_board_hints(row_sibling, column_sibling, hidden_board, visible_board)

def minesweeper_finished(board, num_of_bombs):
    num_of_rows = len(board)
    num_of_columns = len(board[0])
    num_of_cells = num_of_rows * num_of_columns
    for row in range(num_of_rows):
        for column in range(num_of_columns):
            if board[row][column] != HIDDEN_CELL:
                num_of_cells -= 1
    return (num_of_cells - num_of_bombs) == 0

def reveal_board(visible_board, hidden_board):
    for row in range(len(visible_board)):
        for column in range(len(visible_board[0])):
            visible_board[row][column] = UNICODE_SYMBOLS[hidden_board[row][column]]