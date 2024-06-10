#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def hangman_template(errors : list, guessed : list, word : str) -> str:
    """
    plantilla que crea a partir de una palabra y dos listas con aciertos y errors
    la figura del juego del Ahorcado.
    Parámetro:
        lista_errores: lista con las letras que
    """

    person = ("O", "|", "/", "\\", "/ '", "\\")
    gallow = ["  ", "  ", "  ", "  ", "  ", "  "]

    for i in range(len(errors)):
        gallow[i] = person[i]

    gallow_template = "*-------*\n"
    gallow_template += "||      |    \n"
    gallow_template += "||     {0}    \n".format(gallow[0])
    gallow_template += "||   {1} {0} {2}  \n".format(gallow[1], gallow[2], gallow[3])
    gallow_template += "||   {0} {1}   \n".format(gallow[4], gallow[5])
    gallow_template += "||           \n"
    gallow_template += "||=========\n\n"

    gallow_template += "word:"
    for letter in word:
        if letter not in guessed:
            gallow_template += " _"
        else:
            gallow_template += letter
    return gallow_template


def is_valid_letter(letra: str) -> bool:
    return letra.isalpha() and len(letra) == 1
