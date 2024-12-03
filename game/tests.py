import unittest

from game.balda_model import GameModel


class TestGameModel(unittest.TestCase):
    def setUp(self):
        self.model = GameModel()

    def test_initial_setup(self):
        self.assertEqual(self.model.board[2], list("БАЛДА"))
        self.assertEqual(self.model.scores, [0, 0])
        self.assertEqual(self.model.current_player, 0)

    def test_add_letter(self):
        self.model.add_letter(0, 0, "А")
        self.assertEqual(self.model.board[0][0], "А")

    def test_invalid_add_letter(self):
        with self.assertRaises(ValueError):
            self.model.add_letter(2, 2, "А")  # Клетка занята

    def test_add_word(self):
        self.model.add_word("БАЛДА")
        self.assertIn("БАЛДА", self.model.word_list)
        self.assertEqual(self.model.scores[0], 5)

    def test_repeated_word(self):
        self.model.add_word("БАЛДА")
        with self.assertRaises(ValueError):
            self.model.add_word("БАЛДА")

    def test_game_over(self):
        for y in range(5):
            for x in range(5):
                if y != 2:
                    self.model.add_letter(x, y, "А")
        self.assertTrue(self.model.is_game_over())
