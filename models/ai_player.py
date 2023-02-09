from abc import abstractmethod
from models.player import Player


class AIPlayer(Player):
    @abstractmethod
    def __init__(self, name, id):
        super().__init__(name, id)

    def make_move(self, board):
        """Choose the best move using the minimax algorithm"""
        pass
