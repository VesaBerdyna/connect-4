from models.ai_player import AIPlayer
from enums.player_type import PlayerType
import random


class RandomAI(AIPlayer):
    def __init__(self, name, id=None):
        super().__init__(name, id)
        self.type = PlayerType.RandomAI.value

    def make_move(self, board, dot):
        valid_moves = board.valid_moves()
        random_col = random.choice(valid_moves)
        row = board.get_next_open_row(random_col)
        board.drop_dot(row, random_col, dot)


class MinimaxAI(AIPlayer):
    def __init__(
        self,
        name: str,
        id=None,
        depth=3,
    ):
        super().__init__(name, id)
        self.type = PlayerType.MiniMaxAI.value
        self.depth = depth

    def make_move(self, board, dot, opponent_dot):
        col = self.minimax(board, self.depth, True, dot, opponent_dot)
        if col >= 0:
            row = board.get_next_open_row(col)
            board.drop_dot(row, col, dot)

    def minimax(self, board, depth, isMaximizing, dot, opponent_dot):
        if board.winning_move(board.board, dot):
            return 1 if isMaximizing else -1
        elif board.winning_move(board.board, opponent_dot):
            if depth == 1:
                return -float("inf")
            else:
                return -1 if isMaximizing else 1
        elif depth == 0:
            return 0
        if isMaximizing:
            bestScore = -float("inf")
            bestMove = None
            for col in range(board.COLUMN_COUNT):
                row = board.get_next_open_row(col)
                if row is not None:
                    board.drop_dot(row, col, dot)
                    score = self.minimax(board, depth - 1, False, dot, opponent_dot)
                    if score > bestScore:
                        bestScore = score
                        bestMove = col
                    board.board[row][col] = None
            return bestMove
        else:
            bestScore = float("inf")
            bestMove = None
            for col in range(board.COLUMN_COUNT):
                row = board.get_next_open_row(col)
                if row is not None:
                    board.drop_dot(row, col, opponent_dot)
                    score = self.minimax(board, depth - 1, True, dot, opponent_dot)
                    if score < bestScore:
                        bestScore = score
                        bestMove = col
                    board.board[row][col] = None
            return bestMove
