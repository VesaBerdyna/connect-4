from models.player import Player


class HumanPlayer(Player):
    def __init__(self, name, id=None):
        super().__init__(name, id)

    def make_move(self, board, row, col, dot):
        """Ask the player for a move and make it on the game board"""
        board.drop_dot(row, col, dot)

    def to_dict(self):
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_dict(cls, data):
        id = data.get("id")
        name = data.get("name")
        return cls(name=name, id=id)
