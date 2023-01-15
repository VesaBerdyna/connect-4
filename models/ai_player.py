from abc import abstractmethod
from models.player import Player


class AIPlayer(Player):
    @abstractmethod
    def __init__(self, name, depth):
        super().__init__(name)
        self.depth = depth

    @abstractmethod
    def make_move(self, board):
        """Choose the best move using the minimax algorithm"""
        pass


# This implementation uses the minimax algorithm with alpha-beta pruning to choose the best move. The make_move() method loops through all the valid moves on the game board, simulates the move by creating a copy of the game board and dropping a piece, and uses the _minimax() method to evaluate the score of the move. The move with the highest score is chosen as the best move, and the piece is dropped on the original game board.

# The _minimax() method is a recursive function that implements the minimax algorithm with alpha-beta pruning. It starts by checking if the depth limit has been reached or if the game is over. If so, it returns the score of the game board using the evaluate() method.

# Otherwise, it checks if it's the maximizing player's turn or
