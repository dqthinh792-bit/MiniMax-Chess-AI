import unittest

import chess

from MiniMax import choose_move, evaluate_board, minimax


class ChessEngineTests(unittest.TestCase):
    def test_start_position_has_20_legal_moves(self):
        board = chess.Board()
        self.assertEqual(len(list(board.legal_moves)), 20)

    def test_evaluation_is_neutral_at_start(self):
        self.assertEqual(evaluate_board(chess.Board()), 0)

    def test_easy_move_is_legal(self):
        board = chess.Board()
        move = choose_move(board, "Easy")
        self.assertIn(move, board.legal_moves)

    def test_medium_move_is_legal(self):
        board = chess.Board()
        move = choose_move(board, "Medium")
        self.assertIn(move, board.legal_moves)

    def test_minimax_returns_legal_move(self):
        board = chess.Board()
        move = minimax(1, True, -200000, 200000, board, True)
        self.assertIn(move, board.legal_moves)

    def test_search_restores_board_state(self):
        board = chess.Board()
        before = board.fen()
        minimax(2, True, -200000, 200000, board, True)
        self.assertEqual(board.fen(), before)


if __name__ == "__main__":
    unittest.main()
