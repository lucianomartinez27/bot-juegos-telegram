import pytest
from games.Connect4.connect4 import Connect4Game, AgainstComputerConnect4
from utils.errors import ModelError

def test_connect4_initialization():
    game = Connect4Game()
    assert game.rows == 6
    assert game.cols == 7
    assert len(game.board) == 6
    assert len(game.board[0]) == 7
    assert game.game_finished == False

def test_connect4_mark_column():
    game = Connect4Game()
    game.mark_column('🔴', 0)
    assert game.board[5][0] == '🔴'
    assert game.last_movement_symbol == '🔴'

def test_connect4_mark_column_stacking():
    game = Connect4Game()
    game.mark_column('🔴', 0)
    game.mark_column('🟡', 0)
    assert game.board[5][0] == '🔴'
    assert game.board[4][0] == '🟡'

def test_connect4_invalid_column():
    game = Connect4Game()
    with pytest.raises(ModelError):
        game.mark_column('🔴', 7)

def test_connect4_full_column():
    game = Connect4Game()
    for _ in range(3):
        game.mark_column('🔴', 0)
        game.mark_column('🟡', 0)
    with pytest.raises(ModelError):
        game.mark_column('🔴', 0)

def test_connect4_horizontal_win():
    game = Connect4Game()
    for i in range(4):
        game.board[5][i] = '🔴'
    assert game.is_winner('🔴') == True

def test_connect4_vertical_win():
    game = Connect4Game()
    for i in range(4):
        game.board[i][0] = '🔴'
    assert game.is_winner('🔴') == True

def test_connect4_diagonal_win_positive():
    game = Connect4Game()
    for i in range(4):
        game.board[5-i][i] = '🔴'
    assert game.is_winner('🔴') == True

def test_connect4_diagonal_win_negative():
    game = Connect4Game()
    for i in range(4):
        game.board[i][i] = '🔴'
    assert game.is_winner('🔴') == True

def test_connect4_no_win():
    game = Connect4Game()
    assert game.is_winner('🔴') == False

def test_connect4_json_serialization():
    game = Connect4Game()
    game.mark_column('🔴', 0)
    json_str = game.to_json()
    new_game = Connect4Game.from_json(json_str)
    assert new_game.board[5][0] == '🔴'
    assert new_game.last_movement_symbol == '🔴'

def test_ai_wins_if_possible():
    game = AgainstComputerConnect4(player_symbol='🔴', computer_symbol='🟡')
    #🟡🟡🟡
    game.board[5][0] = '🟡'
    game.board[5][1] = '🟡'
    game.board[5][2] = '🟡'
    game.last_movement_symbol = '🔴' # it's computer's turn
    game.make_computer_movement()
    assert game.board[5][3] == '🟡'
    assert game.game_finished == True

def test_ai_blocks_player_win():
    game = AgainstComputerConnect4(player_symbol='🔴', computer_symbol='🟡')
    #🔴🔴🔴
    game.board[5][0] = '🔴'
    game.board[5][1] = '🔴'
    game.board[5][2] = '🔴'
    game.last_movement_symbol = '🔴' # it's computer's turn
    game.make_computer_movement()
    assert game.board[5][3] == '🟡'
