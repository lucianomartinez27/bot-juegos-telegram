#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def plantilla_ahorcado(lista_errores, lista_aciertos, palabra):
    """
    plantilla que crea a partir de una palabra y dos listas con aciertos y errores
    la figura del juego del ahorcado.
    Parámetro:
        lista_errores: lista con las letras que
    """

    persona = ("O", "|", "/", "\\", "/ '", "\\")
    horca = ["  ", "  ", "  ", "  ", "  ", "  "]

    for i in range(len(lista_errores)):
        horca[i] = persona[i]

    plantilla = "*-------*\n"
    plantilla += "||      |    \n"
    plantilla += "||     {0}    \n".format(horca[0])
    plantilla += "||   {1} {0} {2}  \n".format(horca[1], horca[2], horca[3])
    plantilla += "||   {0} {1}   \n".format(horca[4], horca[5])
    plantilla += "||           \n"
    plantilla += "||=========\n\n"

    plantilla += "Palabra:"
    for letra in palabra:
        if letra not in lista_aciertos:
            plantilla += " _"
        else:
            plantilla += letra
    return plantilla
