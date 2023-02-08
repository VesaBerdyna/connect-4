import json
import uuid
from abc import ABC, abstractmethod
from random import choice

from enums.game_status import GameStatus
from enums.player_type import PlayerType
from models.board import Board
from models.dot import Dot


class GameInterface(ABC):
    @abstractmethod
    def get_current_turn(self):
        pass

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def set_player_dot(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def winning_move(self, dot):
        pass

    @abstractmethod
    def get_game_state(self):
        pass


class Game(GameInterface):
    def __init__(self, player_one, player_two):
        self.__id = str(uuid.uuid4())
        self.player_one = player_one
        self.player_two = player_two
        self.current_turn = self.player_one
        self.remaining_moves = 42
        self.board = Board()
        self.status = GameStatus.CREATED
        self.default_dots = [Dot("VIOLET", "#6c44a4"), Dot("BLUE", "#0000FF")]
        self.players_dots = {}
        self.game_result = ""
        self.players = {}

    def get_current_turn(self):
        return self.current_turn

    def get_id(self):
        return self.__id

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
        self.status = GameStatus.STARTED
        print(f"Game status is: {self.status.value}")

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

    def get_game_state(self):
        self.players["players"] = {
            f"{self.player_one.id}": self.players_dots[self.player_one.id].name,
            f"{self.player_two.id}": self.players_dots[self.player_two.id].name,
        }
        if self.player_two.name == "Bot":
            bot = True
        else:
            bot = False

        game_json = {
            "current_turn": self.current_turn.id,
            "board": self.board.board,
            "game_result": self.game_result,
            "player_one_id": self.player_one.id,
            "player_two_id": self.player_two.id,
            "remaining_moves": self.remaining_moves,
            "players": self.players,
            "bot": bot,
        }

        game_json = json.dumps(game_json)
        print(game_json)
        return game_json

    def play(self, player, col):
        if self.game_result != "":
            return "Game result already declared."
        else:
            row = self.board.get_next_open_row(col)
            if row is not None:
                if player.type == PlayerType.RandomAI.value:
                    player.make_move(self.board, self.players_dots[player.id].name)

                elif player.type == PlayerType.MiniMaxAI.value:
                    player_name = self.players_dots[player.id].name

                    for key, value in self.players_dots.items():
                        if self.players_dots[key].name == player_name:
                            continue
                        opponent_id = key
                    opponent_dot = self.players_dots[opponent_id].name
                    player.make_move(
                        self.board, self.players_dots[player.id].name, opponent_dot
                    )

                else:
                    player.make_move(
                        self.board, row, col, self.players_dots[player.id].name
                    )
                if self.winning_move(self.players_dots[player.id]):
                    self.game_result = f"{player.name}"
                    self.status = GameStatus.FINISHED
                    print(f"Game status is: {self.status.value}")
                    print(self.game_result)
                    return 0
            self.switchCurrentPlayer()
            self.remaining_moves -= 1
            if self.remaining_moves <= 0:
                self.game_result = "DRAW"
            print(self.board.board)

            return None

    def switchCurrentPlayer(self):
        if self.current_turn == self.player_one:
            self.current_turn = self.player_two
            return
        self.current_turn = self.player_one
