from models.ai_player import AIPlayer
from enums.player_type import PlayerType
import random
from copy import deepcopy


class RandomAI(AIPlayer):
    def __init__(self, name, id=None):
        super().__init__(name, id)
        self.type = PlayerType.RandomAI.value

    def to_dict(self):
        return {"id": self.id, "name": self.name, "type": self.type}

    @classmethod
    def from_dict(cls, data):
        id = data.get("id")
        name = data.get("name")
        return cls(name=name, id=id)
        
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
        depth=1,
    ):
        super().__init__(name, id)
        self.type = PlayerType.MiniMaxAI.value
        self.depth = depth

    def to_dict(self):
        return {"id": self.id, "name": self.name, "type": self.type}

    @classmethod
    def from_dict(cls, data):
        id = data.get("id")
        name = data.get("name")
        return cls(name=name, id=id)

    def make_move(self, board, row, col, dot):
        """Choose the best move using the minimax algorithm with alpha-beta pruning"""
        best_move = None
        best_score = float("-inf")
        alpha = float("-inf")
        beta = float("inf")
        for move in board.valid_moves():
            # make a copy of the game board to simulate the move
            simulated_board = board.copy()
            simulated_board.drop_dot(row, col, dot)
            score = self._minimax(simulated_board, self.depth, alpha, beta, False)
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, score)
        board.drop_piece(best_move, self)

    def _minimax(self, board, depth, alpha, beta, is_maximizing, row, col, dot):
        """Recursive function to implement the minimax algorithm with alpha-beta pruning"""
        if depth == 0 or board.game_over():
            return board.evaluate(self)

        if is_maximizing:
            max_score = float("-inf")
            for move in board.valid_moves():
                simulated_board = board.copy()
                simulated_board.drop_dot(row, col, dot)
                score = self._minimax(simulated_board, depth - 1, alpha, beta, False)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break  # beta cut-off
            return max_score
        else:
            min_score = float("inf")
            for move in board.valid_moves():
                simulated_board = board.copy()
                simulated_board.drop_dot(row, col, dot)
                score = self._minimax(simulated_board, depth - 1, alpha, beta, True)
                min_score = min(min_score, score)
                beta = min(beta, score)
                if beta <= alpha:
                    break  # alpha cut-off
            return min_score
