# Ta Te Ti

import random


def chequear_letra_jugador(letra):
    if letra.upper() == 'X':
        return ("X", "O")
    elif letra.upper() == 'O':
        return ("O", "X")
    else:
        return None


def hacer_jugada(tablero, letra, jugada):
    tablero[jugada] = letra


def es_ganador(ta, le):
    # Dado un tablero y la letra de un jugador, devuelve True (verdadero) si el mismo ha ganado.
    # Utilizamos reempplazamos tablero por ta y letra por le para no escribir tanto
    return ((ta[6] == le and ta[7] == le and ta[8] == le) or  # horizontal superior
            (ta[3] == le and ta[4] == le and ta[5] == le) or  # horizontal medio
            (ta[0] == le and ta[1] == le and ta[2] == le) or  # horizontal inferior
            (ta[6] == le and ta[3] == le and ta[0] == le) or  # verticual izquierda
            (ta[7] == le and ta[4] == le and ta[1] == le) or  # vertical medio
            (ta[8] == le and ta[5] == le and ta[2] == le) or  # vertical derecha
            (ta[6] == le and ta[4] == le and ta[2] == le) or  # diagonal
            (ta[8] == le and ta[4] == le and ta[0] == le))  # diagonal


def obtener_duplicado_tablero(tablero):
    # Duplica la lista del tablero y devuelve el duplicado
    return tablero[:]


def hay_espacio_libre(tablero, jugada):
    # Devuelte true si hay espacio paraefectuar la jugada en el tablero.
    return tablero[jugada] == " "


def elegir_azar_de_lista(tablero, listaJugada):
    # Devuelve una jugada válida en el tablero de la lista recibida.
    # Devuelve None si no hay ninguna jugada válida.

    jugadas_posibles = []
    for i in listaJugada:
        if hay_espacio_libre(tablero, i):
            jugadas_posibles.append(i)

    if len(jugadas_posibles) != 0:
        return random.choice(jugadas_posibles)


def obtener_jugada_computadora(tablero, letra_computadora):
    # Dado un tablero y la letra de la computadora, determina que jugada efectuar.
    if letra_computadora == 'X':
        letra_jugador = 'O'
    else:
        letra_jugador = 'X'

    # Aquí está nuestro algoritmo para nuestra IA (Inteligencia Artificial) del TATETI
    # Primero, verifica si podemos ganar en la próxima jugada.
    for i in range(9):
        copia = obtener_duplicado_tablero(tablero)
        if hay_espacio_libre(copia, i):
            hacer_jugada(copia, letra_computadora, i)
            if es_ganador(copia, letra_computadora):
                tablero[i] = letra_computadora
                return

    # Verifica si el jugador podría ganar en su próxima jugada, y lo bloquea.
    for i in range(9):
        copia = obtener_duplicado_tablero(tablero)
        if hay_espacio_libre(copia, i):
            hacer_jugada(copia, letra_jugador, i)
            if es_ganador(copia, letra_jugador):
                tablero[i] = letra_computadora
                return

    # Intenta ocupar una de las esquinas de estar libre.
    jugada = elegir_azar_de_lista(tablero, [0, 2, 6, 8])
    if jugada != None:
        tablero[jugada] = letra_computadora
        return

    # De estar libre, intenta ocupar el centro.
    if hay_espacio_libre(tablero, 4):
        tablero[4] = letra_computadora
        return

    # Ocupa alguno de los lados.
    i = elegir_azar_de_lista(tablero, [1, 3, 5, 7])
    tablero[i] = letra_computadora


def tablero_completo(tablero):
    # D evuelve True si cada espacio del tablero fue ocupado, caso contrario devuelve False.
    for i in range(9):
        if hay_espacio_libre(tablero, i):
            return False
    return True
