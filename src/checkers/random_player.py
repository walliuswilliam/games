import random

class RandomPlayer:
    def __init__(self):
        self.color = 1

    def make_move(self, board):
        valid_moves = board.get_valid_moves(self.color)
        if valid_moves:
            move = random.choice(valid_moves)
            start, end = move
            board.move_piece(start, end)
            board.check_promotion(end)
            board.check_capture(end)

    def get_valid_moves(self, color):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == color:
                    if color == 1 or color == 3:
                        if j < 7 and self.board[i+1][j+1] == 0:
                            valid_moves.append(((i, j), (i+1, j+1)))
                        if j > 0 and self.board[i+1][j-1] == 0:
                            valid_moves.append(((i, j), (i+1, j-1)))