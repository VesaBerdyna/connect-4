import uuid
from models.board import Board
from models.dot import Dot
from models.person import Person
from random import choice
import json
from models.game_db import GameDB


class Game:
    game_db = GameDB("GAME")

    def __init__(self, player_one: Person):
        self.__id = str(uuid.uuid4())
        self.player_one = player_one
        self.player_two = ""
        self.current_turn = self.player_one
        self.remaining_moves = 42
        self.board = Board()
        self.status = ""
        self.default_dots = [Dot("RED", "#FF0000"), Dot("BLUE", "#0000FF")]
        self.players_dots = {}
        self.game_result = ""
        self.players = {}

    def set_players(self):
        return {
            self.player_one.id: self.player_one,
            self.player_two.id: self.player_two,
        }

    def get_current_turn(self):
        return self.current_turn

    def get_id(self):
        return self.__id

    def connect_player_two(self, player_two):
        self.player_two = player_two

    def set_player_dot(self):
        first_dot = choice(self.default_dots)
        self.players_dots[self.player_one.id] = first_dot
        self.default_dots.remove(first_dot)
        self.players_dots[self.player_two.id] = self.default_dots[0]
        self.default_dots.clear()

        print(
            f"Player {self.player_one.name} has: {self.players_dots[self.player_one.id].name}"
        )
        print(
            f"Player {self.player_two.name} has: {self.players_dots[self.player_two.id].name}"
        )

    def start(self):
        if self.player_one is None or self.player_two is None:
            raise ValueError
        self.status = "playing"
        print("Game has started!")