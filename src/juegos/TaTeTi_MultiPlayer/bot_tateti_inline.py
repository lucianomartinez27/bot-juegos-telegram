from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import os
from juegos.TaTeTi.bot_tictactoe import BotTicTacToe


class BotTaTeTiInLine(BotTicTacToe):
    def __init__(self):
        super(BotTicTacToe, self).__init__(__file__)

    def es_inline(self):
        return True

    def nombre(self):
        return 'TaTeTi_MultiPlayer'

    def generar_datos(self, id_usuario):
        # id_usuario se convierte en string porque las claves json deben ser de ese tipo
        return {'usuarios': {id_usuario: {'letra_jugador': 'X'}}, 'tablero': [" " for i in range(9)],
                'partida_terminada': False}

    def generar_markup(self, update, context):
        opciones = [[InlineKeyboardButton(" ", callback_data="{}".format(i))
                     for i in j] for j in [[0, 1, 2], [3, 4, 5], [6, 7, 8]]]
        return InlineKeyboardMarkup(opciones)

    def responder_boton(self, update, context):
        casilla = int(update.callback_query.data)
        id_usuario = str(self.generar_id_usuario(update))
        bot = context.bot
        id_mensaje = update.callback_query.inline_message_id
        self.datos_usuarios.setdefault(id_mensaje, self.generar_datos(id_usuario))
        self.data_manager.save_info(self.datos_usuarios)
        self.asignar_letra_a_oponente(id_mensaje, id_usuario)

        letra = self.datos_usuarios[id_mensaje]['usuarios'][id_usuario]['letra_jugador']
        tablero = self.datos_usuarios[id_mensaje]['tablero']
        self.marcar_casillero(bot, casilla, id_mensaje, letra, tablero)

    def marcar_casillero(self, bot, casilla, id_mensaje, letra, tablero):
        if self.es_el_turno_del_jugador(letra, tablero):
            self.actualizar_tablero(bot, casilla, id_mensaje, letra, tablero)

    def es_el_turno_del_jugador(self, letra, tablero):
        return letra == 'X' and tablero.count(' ') % 2 != 0 or \
               tablero.count(' ') % 2 == 0 and letra == 'O'

    def asignar_letra_a_oponente(self, id_mensaje, id_usuario):
        if self.solo_ha_jugado_x(id_mensaje, id_usuario):
            self.datos_usuarios[id_mensaje]['usuarios'].update({id_usuario: {'letra_jugador': 'O'}})

    def solo_ha_jugado_x(self, id_mensaje, id_usuario):
        return self.datos_usuarios[id_mensaje]['tablero'].count('X') == 1 and \
               self.datos_usuarios[id_mensaje]['tablero'].count('O' == 0) \
               and id_usuario not in self.datos_usuarios[id_mensaje]['usuarios'] \
               and len(self.datos_usuarios[id_mensaje]['usuarios'] < 2)
