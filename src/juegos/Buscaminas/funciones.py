#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import copy

dic_unicode = {0: " ", 1: u"\U00000031", 2: u"\U00000032", 3: u"\U00000033", 4: u"\U00000034",
                   5: u"\U00000035",
                   6: u"\U00000036", 7: u"\U00000037", 8: u"\U00000038", 9: u"\U0001F4A3"}

def crear_tablero(filas, columnas, total_bombas):
    tablero = []
    bombas_colocadas = 0
    for i in range(filas):
        tablero.append([])
        for j in range(columnas):
                tablero[i].append(0)
    while bombas_colocadas < total_bombas:
        x = random.randrange(filas)
        y = random.randrange(columnas)
        if tablero[x][y] != 9:
            tablero[x][y] = 9
            bombas_colocadas += 1
    return colocar_pistas(tablero)

def tablero_visible_inicial(tablero):
    tablero2 = copy.deepcopy(tablero)
    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            tablero2[i][j] = u"\U00002B1C"
    return tablero2

def colocar_pistas(tablero):
    fil = len(tablero)
    col = len(tablero[0])
    for y in range(fil):
        for x in range(col):
            if tablero[y][x] == 9:
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if 0 <= y+i <= fil-1 and 0 <= x+j <= col-1:
                            if tablero[y+i][x+j] != 9:
                                tablero[y+i][x+j] += 1
    return tablero

def tablero_unicode(tablero):
    dic_unicode = {0: u"\U00000030", 1:u"\U00000031", 2:u"\U00000032", 3:u"\U00000033", 4:u"\U00000034", 5:u"\U00000035",
                   6: u"\U00000036", 7:u"\U00000037", 8:u"\U00000038", 9: u"\U0001F4A3"}
    tablero_u = tablero[:]

    for i in range(len(tablero)):
        for j in range(len(tablero[i])):
            try:
                tablero[i][j] = dic_unicode[tablero[i][j]]
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

def verificar_tablero(tablero, bombas):
    filas = len(tablero)
    columas = len(tablero[0])
    total_casillas = filas * columas
    for i in range(filas):
        for j in range(columas):
            if tablero[i][j] != u"\U00002B1C":
                total_casillas -= 1
    return total_casillas - bombas == 0

def descubrir_tablero(t_visible, t_oculto):
        for i in range(len(t_visible)):
            for j in range(len(t_visible[0])):
                t_visible[i][j] = dic_unicode[t_oculto[i][j]]