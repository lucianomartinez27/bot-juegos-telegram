#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def plantilla_ahorcado(lista_errores : list, lista_aciertos : list, palabra : str) -> str:
    """
    plantilla que crea a partir de una palabra y dos listas con aciertos y errores
    la figura del juego del Ahorcado.
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


def letra_valida(letra: str) -> bool:
    return letra.isalpha() and len(letra) == 1
