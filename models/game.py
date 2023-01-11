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
        
    def winning_move(self, dot):
        # Check horizontal locations for win
        for c in range(self.board.COLUMN_COUNT - 3):
            for r in range(self.board.ROW_COUNT):
                if (
                    self.board.board[r][c] == dot.name
                    and self.board.board[r][c + 1] == dot.name
                    and self.board.board[r][c + 2] == dot.name
                    and self.board.board[r][c + 3] == dot.name
                ):
                    return True

        # Check vertical locations for win
        for c in range(self.board.COLUMN_COUNT):
            for r in range(self.board.ROW_COUNT - 3):
                if (
                    self.board.board[r][c] == dot.name
                    and self.board.board[r + 1][c] == dot.name
                    and self.board.board[r + 2][c] == dot.name
                    and self.board.board[r + 3][c] == dot.name
                ):
                    return True

        # Check positively sloped diaganols
        for c in range(self.board.COLUMN_COUNT - 3):
            for r in range(self.board.ROW_COUNT - 3):
                if (
                    self.board.board[r][c] == dot.name
                    and self.board.board[r + 1][c + 1] == dot.name
                    and self.board.board[r + 2][c + 2] == dot.name
                    and self.board.board[r + 3][c + 3] == dot.name
                ):
                    return True

        # Check negatively sloped diaganols
        for c in range(self.board.COLUMN_COUNT - 3):
            for r in range(3, self.board.ROW_COUNT):
                if (
                    self.board.board[r][c] == dot.name
                    and self.board.board[r - 1][c + 1] == dot.name
                    and self.board.board[r - 2][c + 2] == dot.name
                    and self.board.board[r - 3][c + 3] == dot.name
                ):
                    return True
                
    def updateDB(self):
        move = {
            "current_turn": self.current_turn.id,
            "board": self.board.board,
            "game_result": self.game_result,
            "player_one_id": self.player_one.id,
            "player_two_id": self.player_two.id,
            "remaining_moves": self.remaining_moves,
        }

        final_move = json.dumps(move)
        print(final_move)
        self.game_db.add_move(self.__id, final_move)

    def retrieveSave(self):
        save = self.game_db.getMove()
        if save:
            return save
        else:
            return "FAIL"

    def move(self, player, col):
        if self.game_result != "":
            return "Game result already declared."
        else:
            print("HELO")
            print(player)
            print(self.players_dots[player.id])
            if self.board.is_valid_location(col):
                row = self.board.get_next_open_row(col)
                self.board.drop_dot(row, col, self.players_dots[player.id].name)

            if self.winning_move(self.players_dots[player.id]):
                self.game_result = f"{player.name} wins!!!!"
                print(self.game_result)
                return
            self.switchCurrentPlayer()
            self.remaining_moves -= 1
            if self.remaining_moves <= 0:
                self.game_result = "DRAW"
            print(self.board.board)

            self.updateDB()
            return None

    def switchCurrentPlayer(self):
        if self.current_turn == self.player_one:
            self.current_turn = self.player_two
            return
        self.current_turn = self.player_one
        
