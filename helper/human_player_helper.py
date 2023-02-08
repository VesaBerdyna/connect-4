class HumanPlayerHelper:
    @classmethod
    def get_suggested_move(cls, board, player_dot, opponent_dot):
        board = list(reversed(board))
        rows, cols = len(board), len(board[0])
        
        # Check rows for opponent win
        for row in range(rows):
            for col in range(cols - 2):
                if (
                    board[row][col] == player_dot
                    and board[row][col + 1] == player_dot
                    and board[row][col + 2] == player_dot
                ):
                    if col > 0 and board[row][col - 1] == None:
                        return (row, col - 1)
                    elif col < cols - 3 and board[row][col + 3] == None:
                        return (row, col + 3)

            # Check cols for player win
        for col in range(cols):
            for row in range(rows - 2):
                if (
                    board[row][col] == player_dot
                    and board[row + 1][col] == player_dot
                    and board[row + 2][col] == player_dot
                ):
                    if row > 0 and board[row - 1][col] == None:
                        return (row - 1, col)
                    elif row < rows - 3 and board[row + 3][col] == None:
                        return (row + 3, col)

        # Check diagonal (top-left to bottom-right) for player win
        for row in range(rows - 2):
            for col in range(cols - 2):
                if (
                    board[row][col] == player_dot
                    and board[row + 1][col + 1] == player_dot
                    and board[row + 2][col + 2] == player_dot
                ):
                    if row > 0 and col > 0 and board[row - 1][col - 1] == None:
                        return (row - 1, col - 1)
                    elif (
                        row < rows - 3
                        and col < cols - 3
                        and board[row + 3][col + 3] == None
                    ):
                        return (row + 3, col + 3)

        # Check diagonal (bottom-left to top-right) for player win
        for row in range(rows - 2, 0, -1):
            for col in range(cols - 2):
                if (
                    board[row][col] == player_dot
                    and board[row - 1][col + 1] == player_dot
                    and board[row - 2][col + 2] == player_dot
                ):
                    if row < rows - 1 and col > 0 and board[row + 1][col - 1] == None:
                        return (row + 1, col - 1)
                    elif row > 2 and col < cols - 3 and board[row - 3][col + 3] == None:
                        return (row - 3, col + 3)
        # Check rows for opponent win
        for row in range(rows):
            for col in range(cols - 2):
                if (
                    board[row][col] == opponent_dot
                    and board[row][col + 1] == opponent_dot
                    and board[row][col + 2] == opponent_dot
                ):
                    if col > 0 and board[row][col - 1] == None:
                        return (row, col - 1)
                    elif col < cols - 3 and board[row][col + 3] == None:
                        return (row, col + 3)

        # Check cols for opponent win
        for col in range(cols):
            for row in range(rows - 2):
                if (
                    board[row][col] == opponent_dot
                    and board[row + 1][col] == opponent_dot
                    and board[row + 2][col] == opponent_dot
                ):
                    if row > 0 and board[row - 1][col] == None:
                        return (row - 1, col)
                    elif row < rows - 3 and board[row + 3][col] == None:
                        return (row + 3, col)

        # Check diagonal (top-left to bottom-right) for opponent win
        for row in range(rows - 2):
            for col in range(cols - 2):
                if (
                    board[row][col] == opponent_dot
                    and board[row + 1][col + 1] == opponent_dot
                    and board[row + 2][col + 2] == opponent_dot
                ):
                    if row > 0 and col > 0 and board[row - 1][col - 1] == None:
                        return (row - 1, col - 1)
                    elif (
                        row < rows - 3
                        and col < cols - 3
                        and board[row + 3][col + 3] == None
                    ):
                        return (row + 3, col + 3)

        # Check diagonal (bottom-left to top-right) for opponent win
        for row in range(rows - 2, 0, -1):
            for col in range(cols - 2):
                if (
                    board[row][col] == opponent_dot
                    and board[row - 1][col + 1] == opponent_dot
                    and board[row - 2][col + 2] == opponent_dot
                ):
                    if row < rows - 1 and col > 0 and board[row + 1][col - 1] == None:
                        return (row + 1, col - 1)
                    elif row > 2 and col < cols - 3 and board[row - 3][col + 3] == None:
                        return (row - 3, col + 3)

        # No suggested move found
        return None
