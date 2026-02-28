from games.RockPaperScissor.rock_paper_scissor import RockPaperScissorGame, Rock, Paper, Scissor, NoElement

def test_rock_beats_scissors():
    game = RockPaperScissorGame(Rock(), Scissor())
    assert game.play() == 'rock'
    assert game.last_winner_is_player_one()

def test_paper_beats_rock():
    game = RockPaperScissorGame(Paper(), Rock())
    assert game.play() == 'paper'
    assert game.last_winner_is_player_one()

def test_scissors_beats_paper():
    game = RockPaperScissorGame(Scissor(), Paper())
    assert game.play() == 'scissors'
    assert game.last_winner_is_player_one()

def test_tie():
    game = RockPaperScissorGame(Rock(), Rock())
    assert game.play() == 'tie'
    assert not game.last_winner_is_player_one()

def test_no_element_tie():
    game = RockPaperScissorGame(NoElement(), NoElement())
    assert game.play() == 'tie'

def test_element_factory():
    assert isinstance(RockPaperScissorGame.element('rock'), Rock)
    assert isinstance(RockPaperScissorGame.element('paper'), Paper)
    assert isinstance(RockPaperScissorGame.element('scissors'), Scissor)
    assert isinstance(RockPaperScissorGame.element('unknown'), NoElement)
