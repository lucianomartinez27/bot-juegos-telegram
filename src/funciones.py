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


def pedir_numero(lista_intentos =[]):
    """pide al usuario un número de cuatro cifras y comprueba que no estén en
        una lista donde se guardan intentos"""

    numero_correcto = True
    numeros = input('---> ')

    if numeros.startswith('q'):
        return False

    # Tiene que ser un número de 4 cifras 
    if len(numeros) != 4 or not numeros.isnumeric():
        print('Debes ingresar un numero de 4 cifras.')
        numero_correcto = False
    elif numeros in lista_intentos: # Que no hayamos intentado antes
        print('Ya has intentado con ese número.')
        numero_correcto = False
    else:
        # Números distintos
        sin_repetir = ''
        for i in numeros:
            if i in sin_repetir:
                numero_correcto = False
                print('Los numeros ingresados deben ser todos distintos.\n')
            else:
                sin_repetir += i
    if numero_correcto:
        lista_intentos.append(numeros)
        return numeros

def comprobar_numero(n_computadora, n_usuario, lista_intentos, lista_resultados):
    """comprueba el número de muertos y heridos que obtuvo el usuario"""
    heridos = 0
    muertos = 0
    i = 0
    jugando = True
    for n in n_usuario:
        if n == n_computadora[i]:
            muertos += 1
        elif n in n_computadora:
            heridos += 1
        i += 1

    lista_resultados.append([muertos, heridos])

    os.system('clear')
    print('*' * 10, len(lista_intentos), 'intentos ', '*' *10)
    print('MUERTOS - HERIDOS'.center(30))

    for i in range(len(lista_intentos)):
        print('{}:    {}         {}'.format(lista_intentos[i], lista_resultados[i][0],lista_resultados[i][1]))

    if len(lista_intentos) == 15:
        print('Perdiste!')
        print('El número era:', end =' ')
        for i in n_computadora:
            print(i, end = '')
        jugando = False
        print()

    if muertos == 4:
        print('FELICITACIONES, HAS GANADO')
        jugando = False

    return jugando