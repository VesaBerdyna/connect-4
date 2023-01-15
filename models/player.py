import uuid
from abc import ABC, abstractmethod


class Player(ABC):
    @abstractmethod
    def __init__(self, name, id):
        self.id = str(uuid.uuid4()) if id is None else id
        self.name = name

    @abstractmethod
    def make_move(self, board):
        """Make a move on the game board"""
        pass
