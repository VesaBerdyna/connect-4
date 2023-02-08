from models.player import Player
from enums.player_type import PlayerType


class HumanPlayer(Player):
    def __init__(self, name: str, id=None):
        super().__init__(name, id)
        self.type = PlayerType.HumanPlayer.value

    def make_move(self, board, row, col, dot):
        """Ask the player for a move and make it on the game board"""
        board.drop_dot(row, col, dot)
