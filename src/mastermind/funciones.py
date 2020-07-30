#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import random
import os

def generar_numero():
    """ Genera 4 números aleatorios, del 0 al 9, todos distintos."""
    lista_numeros = []
    while len(lista_numeros) < 4:
        n = random.randint(0, 9)
        if str(n) not in lista_numeros:
            lista_numeros.append(str(n))
    return lista_numeros


def comprobar_numero(numeros, lista_intentos):
    """pide al usuario un número de cuatro cifras y comprueba que no estén en
        una lista donde se guardan intentos"""

    numero_correcto = True

    # Tiene que ser un número de 4 cifras 
    if len(numeros) != 4 or not numeros.isnumeric():
        numero_correcto = False
    elif numeros in lista_intentos: # Que no hayamos intentado antes
        numero_correcto = False
    else:
        # Números distintos
        sin_repetir = ''
        for i in numeros:
            if i in sin_repetir:
                numero_correcto = False
            else:
                sin_repetir += i
    if numero_correcto:
        lista_intentos.append(numeros)
        return numeros
    else:
        return False
def contar_muertos_y_heridos(n_usuario, n_computadora):
    heridos = 0
    muertos = 0
    i = 0
    for n in n_usuario:
        if n == n_computadora[i]:
            muertos += 1
        elif n in n_computadora:
            heridos += 1
        i += 1
    return muertos, heridos

def partida_ganada(n_usuario, n_computadora):
    return contar_muertos_y_heridos(n_usuario, n_computadora) == (4, 0)

def partida_perdida(lista_intentos):
    return len(lista_intentos) > 14

def chequear_numero(n_computadora, n_usuario, lista_intentos, lista_resultados):
    """comprueba el número de muertos y heridos que obtuvo el usuario"""
    
    muertos, heridos = contar_muertos_y_heridos(n_usuario, n_computadora)

    lista_resultados.append([muertos, heridos])

    texto = "Te quedan {} intentos ".format(15-len(lista_intentos))
    texto += '\nMUERTOS - HERIDOS'.center(30)

    for i in range(len(lista_intentos)):
        texto += '\n{}:    {}         {}'.format(lista_intentos[i], lista_resultados[i][0],lista_resultados[i][1])

    return texto