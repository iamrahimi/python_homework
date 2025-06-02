class TictactoeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class Board:
    valid_moves = [
        "upper left", "upper center", "upper right",
        "middle left", "center", "middle right",
        "lower left", "lower center", "lower right"
    ]

    def __init__(self):
        self.board_array = [[" " for _ in range(3)] for _ in range(3)]
        self.turn = "X"
        self.last_move = None

    def __str__(self):
        rows = []
        for i, row in enumerate(self.board_array):
            rows.append(" | ".join(row))
            if i < 2:
                rows.append("-" * 9)
        return "\n".join(rows)

    def move(self, move_string):
        if move_string not in self.valid_moves:
            raise TictactoeException("That's not a valid move.")

        # Map the move string to board indices
        move_map = {
            "upper left": (0, 0),
            "upper center": (0, 1),
            "upper right": (0, 2),
            "middle left": (1, 0),
            "center": (1, 1),
            "middle right": (1, 2),
            "lower left": (2, 0),
            "lower center": (2, 1),
            "lower right": (2, 2),
        }

        row, col = move_map[move_string]

        if self.board_array[row][col] != " ":
            raise TictactoeException("That spot is taken.")

        self.board_array[row][col] = self.turn
        self.last_move = (row, col)

        # Switch turn
        self.turn = "O" if self.turn == "X" else "X"

    def whats_next(self):
        b = self.board_array

        # Check rows, columns, diagonals for a winner
        lines = []

        # Rows and Columns
        for i in range(3):
            lines.append(b[i])  # row
            lines.append([b[0][i], b[1][i], b[2][i]])  # column

        # Diagonals
        lines.append([b[0][0], b[1][1], b[2][2]])
        lines.append([b[0][2], b[1][1], b[2][0]])

        for line in lines:
            if line == ["X", "X", "X"]:
                return True, "X has won"
            if line == ["O", "O", "O"]:
                return True, "O has won"

        # Check for full board (no empty spaces)
        if all(cell != " " for row in b for cell in row):
            return True, "Cat's Game"

        # Game not over
        return False, f"{self.turn}'s turn"


if __name__ == "__main__":
    board = Board()
    print("Welcome to Tic Tac Toe!")
    print(board)
    
    game_over = False
    while not game_over:
        print(f"Current turn: {board.turn}")
        move = input("Enter your move (e.g., 'upper left', 'center'): ").strip().lower()
        try:
            board.move(move)
        except TictactoeException as e:
            print(f"Error: {e.message}")
            continue

        print(board)
        game_over, status = board.whats_next()
        if game_over:
            print(status)