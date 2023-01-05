class Board:
    ROW_COUNT = 6
    COLUMN_COUNT = 7

    def create_empty_matrix(cls):
        board = []
        for i in range(cls.ROW_COUNT):
            row = []
            for j in range(cls.COLUMN_COUNT):
                row.append(None)
            board.append(row)
        return board

    def __init__(self) -> None:
        self.board = self.create_empty_matrix()
        print(self.board)

    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT - 1][col] == None

    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == None:
                print(r)
                return r

    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(col):
                valid_locations.append(col)
        return valid_locations

    def drop_dot(self, row, col, dot):
        self.board[row][col] = dot
