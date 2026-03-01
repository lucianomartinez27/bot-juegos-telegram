from games.Minesweeper.minesweeper import Minesweeper, MINE_CODE, HIDDEN_CELL, UNICODE_SYMBOLS
import json

def test_initialization():
    game = Minesweeper(num_of_rows=5, num_of_cols=5, num_of_bombs=5)
    assert game.num_of_rows == 5
    assert game.num_of_cols == 5
    assert game.num_of_bombs == 5
    assert len(game.hidden_board) == 5
    assert len(game.hidden_board[0]) == 5
    assert len(game.visible_board) == 5
    assert game.game_status == 'playing'
    assert game.bombs_placed == False

def test_first_click_places_bombs():
    game = Minesweeper(num_of_rows=5, num_of_cols=5, num_of_bombs=5)
    assert not game.bombs_placed
    game.mark_cell(2, 2)
    assert game.bombs_placed
    # First clicked cell should NOT be a bomb
    assert game.hidden_board[2][2] != MINE_CODE
    
    # Check if correct number of bombs were placed
    bomb_count = sum(row.count(MINE_CODE) for row in game.hidden_board)
    assert bomb_count == 5

def test_hint_placement():
    game = Minesweeper(num_of_rows=3, num_of_cols=3, num_of_bombs=0)
    # Manually place a bomb
    game.hidden_board[1][1] = MINE_CODE
    game.num_of_bombs = 1
    game.bombs_placed = True
    game.place_hints()
    
    # Check hints around (1,1)
    # 1 1 1
    # 1 B 1
    # 1 1 1
    for r in range(3):
        for c in range(3):
            if (r, c) == (1, 1):
                assert game.hidden_board[r][c] == MINE_CODE
            else:
                assert game.hidden_board[r][c] == 1

def test_lose_on_bomb():
    game = Minesweeper(num_of_rows=3, num_of_cols=3, num_of_bombs=1)
    # Ensure a bomb is at (1,1)
    game.place_bombs(avoid_row=0, avoid_col=0)
    # Find where the bomb actually is
    bomb_pos = None
    for r in range(3):
        for c in range(3):
            if game.hidden_board[r][c] == MINE_CODE:
                bomb_pos = (r, c)
                break
    
    game.mark_cell(*bomb_pos)
    assert game.game_status == 'lose'
    assert game.finished()
    # Check if board revealed
    for r in range(3):
        for c in range(3):
            assert game.visible_board[r][c] != HIDDEN_CELL

def test_win_condition():
    # 2x2 board with 1 bomb at (1,1)
    game = Minesweeper(num_of_rows=2, num_of_cols=2, num_of_bombs=1)
    game.hidden_board = [[0, 0], [0, MINE_CODE]]
    game.place_hints()
    game.bombs_placed = True
    
    # Mark all non-bomb cells
    game.mark_cell(0, 0)
    assert not game.is_winner()
    game.mark_cell(0, 1)
    assert not game.is_winner()
    game.mark_cell(1, 0)
    
    assert game.is_winner()
    assert game.finished()

def test_recursive_reveal_partial():
    # 4x4 board with 2 bombs at (3,3) and (0,3)
    # 0 0 1 B
    # 0 0 1 1
    # 0 0 1 1
    # 0 0 1 B
    game = Minesweeper(num_of_rows=4, num_of_cols=4, num_of_bombs=2)
    game.hidden_board = [
        [0, 0, 1, MINE_CODE],
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 1, MINE_CODE]
    ]
    game.bombs_placed = True
    
    # Click on (0,0) which is 0, should reveal all 0s and their neighbors (column 2)
    # Column 3 should remain hidden
    game.mark_cell(0, 0)
    
    assert game.visible_board[0][0] == UNICODE_SYMBOLS[0]
    assert game.visible_board[0][2] == UNICODE_SYMBOLS[1]
    assert game.visible_board[0][3] == HIDDEN_CELL # Bomb remains hidden
    assert game.visible_board[1][3] == HIDDEN_CELL # Neighbor of bomb but NOT neighbor of any 0
    assert not game.is_winner()
    assert not game.finished()

def test_recursive_reveal_win():
    # 3x3 board with 1 bomb at (2,2)
    # 0 0 0
    # 0 1 1
    # 0 1 B
    game = Minesweeper(num_of_rows=3, num_of_cols=3, num_of_bombs=1)
    game.hidden_board = [[0, 0, 0], [0, 1, 1], [0, 1, MINE_CODE]]
    game.bombs_placed = True
    
    # Click on (0,0) which is 0, should reveal everything and win
    game.mark_cell(0, 0)
    
    assert game.visible_board[0][0] == UNICODE_SYMBOLS[0]
    assert game.visible_board[2][1] == UNICODE_SYMBOLS[1]
    assert game.visible_board[2][2] == UNICODE_SYMBOLS[MINE_CODE] # Bomb revealed because of win
    assert game.is_winner()
    assert game.finished()

def test_serialization():
    game = Minesweeper(num_of_rows=4, num_of_cols=4, num_of_bombs=2)
    game.mark_cell(0, 0)
    
    json_str = game.to_json()
    new_game = Minesweeper.from_json(json_str)
    
    assert new_game.num_of_rows == game.num_of_rows
    assert new_game.num_of_cols == game.num_of_cols
    assert new_game.num_of_bombs == game.num_of_bombs
    assert new_game.hidden_board == game.hidden_board
    assert new_game.visible_board == game.visible_board
    assert new_game.game_status == game.game_status
    assert new_game.bombs_placed == game.bombs_placed

def test_utility_methods():
    game = Minesweeper(num_of_rows=3, num_of_cols=3, num_of_bombs=1)
    game.hidden_board = [[0, 0, 0], [0, MINE_CODE, 0], [0, 0, 0]]
    game.bombs_placed = True
    
    assert game.board() == game.visible_board
    assert not game.finished()
    assert game.is_bomb(1, 1)
    assert not game.is_bomb(0, 0)
    
    game.mark_cell(1, 1)
    assert game.finished()
    assert game.game_status == 'lose'
