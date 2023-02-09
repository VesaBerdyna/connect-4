import uuid
from abc import ABC, abstractmethod


class Player(ABC):
    @abstractmethod
    def __init__(self, name, id):
        self.id = str(uuid.uuid4()) if id is None else id
        self.name = name
        
    def make_move(self, board):
        """Make a move on the game board"""
        pass

    def to_dict(self):
        return {"id": self.id, "name": self.name, "type": self.type}

    @classmethod
    def from_dict(cls, data):
        id = data.get("id")
        name = data.get("name")
        return cls(name=name, id=id)
