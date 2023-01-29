from abc import ABC, abstractmethod


class Board(ABC):
    ROW_COUNT: int
    COLUMN_COUNT: int

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get_next_open_row(self, col: int) -> int:
        pass

    @abstractmethod
    def drop_dot(self, row: int, col: int, dot) -> None:
        pass


class Board:
    ROW_COUNT = 6
    COLUMN_COUNT = 7

    def __init__(self):
        self.board = [
            [None for _ in range(self.COLUMN_COUNT)] for _ in range(self.ROW_COUNT)
        ]

    def get_next_open_row(self, col: int) -> int:
        for r in range(self.ROW_COUNT - 1, -1, -1):
            if self.board[r][col] is None:
                return r
        return None

    def drop_dot(self, row: int, col: int, dot):
        self.board[row][col] = dot
