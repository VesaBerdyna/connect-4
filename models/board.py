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
        
    def is_valid_move(self, col):
        if self.get_next_open_row(col) is not None:
            return True

    def valid_moves(self):
        """
        Get a list of all valid move columns on the board
        """
        valid_moves = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_move(col):
                valid_moves.append(col)
        return valid_moves

    # def winning_move(self, board, dot):
    #     # Check horizontal locations for win
    #     for c in range(self.COLUMN_COUNT - 3):
    #         for r in range(self.ROW_COUNT):
    #             if (
    #                 board[r][c] == dot
    #                 and board[r][c + 1] == dot
    #                 and board[r][c + 2] == dot
    #                 and board[r][c + 3] == dot
    #             ):
    #                 return True

    #     # Check vertical locations for win
    #     for c in range(self.COLUMN_COUNT):
    #         for r in range(self.ROW_COUNT - 3):
    #             if (
    #                 board[r][c] == dot
    #                 and board[r + 1][c] == dot
    #                 and board[r + 2][c] == dot
    #                 and board[r + 3][c] == dot
    #             ):
    #                 return True

    #     # Check positively sloped diaganols
    #     for c in range(self.COLUMN_COUNT - 3):
    #         for r in range(self.ROW_COUNT - 3):
    #             if (
    #                 board[r][c] == dot
    #                 and board[r + 1][c + 1] == dot
    #                 and board[r + 2][c + 2] == dot
    #                 and board[r + 3][c + 3] == dot
    #             ):
    #                 return True

    #     # Check negatively sloped diaganols
    #     for c in range(self.COLUMN_COUNT - 3):
    #         for r in range(3, self.ROW_COUNT):
    #             if (
    #                 board[r][c] == dot
    #                 and board[r - 1][c + 1] == dot
    #                 and board[r - 2][c + 2] == dot
    #                 and board[r - 3][c + 3] == dot
    #             ):
    #                 return True
