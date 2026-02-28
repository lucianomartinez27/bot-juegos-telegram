from games.TicTacToe.tictactoe import AgainstComputerTicTacToe

def test_tictactoe_win_horizontal():
    game = AgainstComputerTicTacToe('X', 'O')
    
    # X X X
    # O O .
    # . . .
    game.mark_cell('X', 0)
    game.mark_cell('O', 3)
    game.mark_cell('X', 1)
    game.mark_cell('O', 4)
    game.mark_cell('X', 2)
    
    assert game.is_winner('X')
    assert game.finished()

def test_tictactoe_draw():
    game = AgainstComputerTicTacToe('X', 'O')
    
    # X O X
    # X O O
    # O X O
    moves = [(0, 'X'), (1, 'O'), (2, 'X'), (4, 'O'), (3, 'X'), (5, 'O'), (7, 'X'), (6, 'O'), (8, 'X')]
    # Wait, the order matters for mark_cell because of last_movement_symbol
    for cell, symbol in [(0, 'X'), (1, 'O'), (2, 'X'), (4, 'O'), (3, 'X'), (5, 'O'), (7, 'X'), (6, 'O')]:
        game.mark_cell(symbol, cell)
    
    # X O X
    # X O O
    # O X .
    # If we mark 8 with X:
    game.mark_cell('X', 8)
    
    assert not game.is_winner('X')
    assert not game.is_winner('O')
    assert game.is_full_board()
    assert game.finished()

def test_computer_blocks_win():
    game = AgainstComputerTicTacToe('X', 'O')
    
    # X X .
    # . . .
    # . . .
    game.mark_cell('X', 0)
    game.mark_cell('O', 4)
    game.mark_cell('X', 1)
    
    # Computer should block at 2
    game.make_computer_movement()
    assert game.board[2] == 'O'

def test_computer_wins_if_possible():
    game = AgainstComputerTicTacToe('X', 'O')
    
    # O O .
    # X X .
    # . . .
    game.mark_cell('O', 0)
    game.mark_cell('X', 3)
    game.mark_cell('O', 1)
    game.mark_cell('X', 4)
    
    game.make_computer_movement()
    assert game.board[2] == 'O'
    assert game.is_winner('O')
