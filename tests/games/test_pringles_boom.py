import unittest
from games.PringlesBoom.pringles_boom import PringlesBoomGame
from utils.errors import ModelError

class TestPringlesBoomGame(unittest.TestCase):
    def test_game_initialization(self):
        game = PringlesBoomGame(player1_id=123, player1_name="Alice")
        self.assertEqual(game.player1_id, 123)
        self.assertEqual(game.player1_name, "Alice")
        self.assertIsNone(game.player2_id)
        self.assertEqual(game.player2_name, "Player 2")
        self.assertEqual(len(game.bombs1), 0)
        self.assertEqual(len(game.bombs2), 0)
        self.assertEqual(game.phase, PringlesBoomGame.PHASE_SETUP)
        self.assertFalse(game.game_finished)

    def test_game_play_flow(self):
        game = PringlesBoomGame(player1_id=1, player2_id=2, player1_name="Alice", player2_name="Bob")
        
        # Setup phase: P1 places 3 bombs on grid 1
        game.place_bomb(1, 0, 1, user_name="Alice")
        game.place_bomb(1, 1, 1)
        game.place_bomb(1, 2, 1)
        self.assertEqual(len(game.bombs1), 3)
        self.assertEqual(game.phase, PringlesBoomGame.PHASE_SETUP)
        
        # Setup phase: P2 places 3 bombs on grid 2
        game.place_bomb(2, 3, 2, user_name="Bob")
        game.place_bomb(2, 4, 2, user_name="Bob")
        game.place_bomb(2, 5, 2, user_name="Bob")
        self.assertEqual(len(game.bombs2), 3)
        self.assertEqual(game.phase, PringlesBoomGame.PHASE_CHOOSING_EMOJI)
        
        # Emoji selection
        game.set_emoji(1, "🍕")
        game.set_emoji(2, "🍩")
        self.assertEqual(game.player1_emoji, "🍕")
        self.assertEqual(game.player2_emoji, "🍩")
        self.assertEqual(game.phase, PringlesBoomGame.PHASE_PLAYING)
        
        # Player 1's turn, picks safe spot on Player 2's grid (grid_num=2)
        game.pick(1, 0, 2)
        self.assertEqual(game.grid2[0], 1)
        self.assertEqual(game.turn, 2)
        
        # Player 2's turn, picks safe spot on Player 1's grid (grid_num=1)
        game.pick(2, 3, 1)
        self.assertEqual(game.grid1[3], 1)
        self.assertEqual(game.turn, 1)
        
        # Player 1's turn, hits a bomb on Player 2's grid (grid_num=2)
        game.pick(1, 3, 2)
        self.assertEqual(game.grid2[3], 2)
        self.assertEqual(game.exploded_count2, 1)
        self.assertEqual(game.turn, 2)
        
        # Errors: wrong turn
        with self.assertRaises(ModelError) as cm:
            game.pick(1, 4, 2)
        self.assertEqual(str(cm.exception), "Wait your turn! ✋")
            
        # Error: pick same spot
        game.pick(2, 0, 1) # Safe
        self.assertEqual(game.turn, 1)
        with self.assertRaises(ModelError):
            game.pick(1, 3, 2)

    def test_win_condition(self):
        game = PringlesBoomGame(player1_id=1, player2_id=2, player1_name="Alice", player2_name="Bob")
        # Setup
        for i in range(3):
            game.place_bomb(1, i, 1, user_name="Alice")
            game.place_bomb(2, i, 2, user_name="Bob")
        
        game.set_emoji(1, "🍣")
        game.set_emoji(2, "🍣")

        # Player 1 hits 3 bombs on Player 2's grid
        game.pick(1, 0, 2) # Hit 1
        game.pick(2, 4, 1) # Player 2 safe move
        game.pick(1, 1, 2) # Hit 2
        game.pick(2, 5, 1) # Player 2 safe move
        game.pick(1, 2, 2) # Hit 3 - Game Over
        
        self.assertTrue(game.game_finished)
        self.assertEqual(game.winner_id, 1)
        self.assertEqual(game.exploded_count2, 3)
        self.assertEqual(game.phase, PringlesBoomGame.PHASE_FINISHED)

if __name__ == '__main__':
    unittest.main()
