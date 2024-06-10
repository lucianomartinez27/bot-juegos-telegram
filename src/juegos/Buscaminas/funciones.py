#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import copy

dic_unicode = {0: " ", 1: u"\U00000031", 2: u"\U00000032", 3: u"\U00000033", 4: u"\U00000034",
                   5: u"\U00000035",
                   6: u"\U00000036", 7: u"\U00000037", 8: u"\U00000038", 9: u"\U0001F4A3"}

def crear_tablero(filas, columnas, total_bombas):
    board = []
    bombas_colocadas = 0
    for i in range(filas):
        board.append([])
        for j in range(columnas):
                board[i].append(0)
    while bombas_colocadas < total_bombas:
        x = random.randrange(filas)
        y = random.randrange(columnas)
        if board[x][y] != 9:
            board[x][y] = 9
            bombas_colocadas += 1
    return colocar_pistas(board)

def tablero_visible_inicial(board):
    tablero2 = copy.deepcopy(board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            tablero2[i][j] = u"\U00002B1C"
    return tablero2

def colocar_pistas(board):
    fil = len(board)
    col = len(board[0])
    for y in range(fil):
        for x in range(col):
            if board[y][x] == 9:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if 0 <= y+i <= fil-1 and 0 <= x+j <= col-1:
                            if board[y+i][x+j] != 9:
                                board[y+i][x+j] += 1
    return board

def tablero_unicode(board):
    dic_unicode = {0: u"\U00000030", 1:u"\U00000031", 2:u"\U00000032", 3:u"\U00000033", 4:u"\U00000034", 5:u"\U00000035",
                   6: u"\U00000036", 7:u"\U00000037", 8:u"\U00000038", 9: u"\U0001F4A3"}
    tablero_u = board[:]

    for i in range(len(board)):
        for j in range(len(board[i])):
            try:
                board[i][j] = dic_unicode[board[i][j]]
            except KeyError:
                pass
    return tablero_u

def despejar_tablero(fila, col, t_oculto, t_visible):
    se_puede_destapar = t_visible[fila][col] == u"\U00002B1C"
    t_visible[fila][col] = dic_unicode[t_oculto[fila][col]]
    if t_oculto[fila][col] == 0 and se_puede_destapar:
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if fila+i in range(len(t_visible)) and col+j in range(len(t_visible[0])):
                    if t_oculto[fila+i][col+j] != 9:
                        despejar_tablero(fila+i, col+j, t_oculto, t_visible)

def verificar_tablero(board, bombas):
    filas = len(board)
    columas = len(board[0])
    total_casillas = filas * columas
    for i in range(filas):
        for j in range(columas):
            if board[i][j] != u"\U00002B1C":
                total_casillas -= 1
    return total_casillas - bombas == 0

def descubrir_tablero(t_visible, t_oculto):
        for i in range(len(t_visible)):
            for j in range(len(t_visible[0])):
                t_visible[i][j] = dic_unicode[t_oculto[i][j]]