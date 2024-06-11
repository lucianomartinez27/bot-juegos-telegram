# Ta Te Ti

import random


def chequear_letra_jugador(letra):
    if letra.upper() == 'X':
        return ("X", "O")
    elif letra.upper() == 'O':
        return ("O", "X")
    else:
        return None


def hacer_jugada(board, letra, jugada):
    board[jugada] = letra


def es_ganador(ta, le):
    # Dado un board y la letra de un jugador, devuelve True (verdadero) si el mismo ha ganado.
    # Utilizamos reempplazamos board por ta y letra por le para no escribir tanto
    return ((ta[6] == le and ta[7] == le and ta[8] == le) or  # horizontal superior
            (ta[3] == le and ta[4] == le and ta[5] == le) or  # horizontal medio
            (ta[0] == le and ta[1] == le and ta[2] == le) or  # horizontal inferior
            (ta[6] == le and ta[3] == le and ta[0] == le) or  # verticual izquierda
            (ta[7] == le and ta[4] == le and ta[1] == le) or  # vertical medio
            (ta[8] == le and ta[5] == le and ta[2] == le) or  # vertical derecha
            (ta[6] == le and ta[4] == le and ta[2] == le) or  # diagonal
            (ta[8] == le and ta[4] == le and ta[0] == le))  # diagonal


def obtener_duplicado_tablero(board):
    # Duplica la lista del board y devuelve el duplicado
    return board[:]


def hay_espacio_libre(board, jugada):
    # Devuelte true si hay espacio paraefectuar la jugada en el board.
    return board[jugada] == " "


def elegir_azar_de_lista(board, listaJugada):
    # Devuelve una jugada válida en el board de la lista recibida.
    # Devuelve None si no hay ninguna jugada válida.

    jugadas_posibles = []
    for i in listaJugada:
        if hay_espacio_libre(board, i):
            jugadas_posibles.append(i)

    if len(jugadas_posibles) != 0:
        return random.choice(jugadas_posibles)


def obtener_jugada_computadora(board, computer_symbol):
    # Dado un board y la letra de la computadora, determina que jugada efectuar.
    if computer_symbol == 'X':
        player_symbol = 'O'
    else:
        player_symbol = 'X'

    # Aquí está nuestro algoritmo para nuestra IA (Inteligencia Artificial) del TATETI
    # Primero, verifica si podemos ganar en la próxima jugada.
    for i in range(9):
        copia = obtener_duplicado_tablero(board)
        if hay_espacio_libre(copia, i):
            hacer_jugada(copia, computer_symbol, i)
            if es_ganador(copia, computer_symbol):
                board[i] = computer_symbol
                return board

    # Verifica si el jugador podría ganar en su próxima jugada, y lo bloquea.
    for i in range(9):
        copia = obtener_duplicado_tablero(board)
        if hay_espacio_libre(copia, i):
            hacer_jugada(copia, player_symbol, i)
            if es_ganador(copia, player_symbol):
                board[i] = computer_symbol
                return board
    
    copia = obtener_duplicado_tablero(board)
    # Intenta ocupar una de las esquinas de estar libre.
    jugada = elegir_azar_de_lista(board, [0, 2, 6, 8])
    if jugada != None:
        board[jugada] = computer_symbol
        return board

    # De estar libre, intenta ocupar el centro.
    if hay_espacio_libre(board, 4):
        board[4] = computer_symbol
        return board

    # Ocupa alguno de los lados.
    i = elegir_azar_de_lista(board, [1, 3, 5, 7])
    board[i] = computer_symbol
    return board


def tablero_completo(board):
    # D evuelve True si cada espacio del board fue ocupado, caso contrario devuelve False.
    for i in range(9):
        if hay_espacio_libre(board, i):
            return False
    return True
