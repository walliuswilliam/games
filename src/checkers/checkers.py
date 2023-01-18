class Checkers:
    def __init__(self, players):
        self.players = players
        self.board = [[(i + j) % 2 * ((j < 3) - (j > 4)) for j in range(8)] for i in range(8)]
        
        
        self.white_kings = []
        self.black_kings = []
        self.turn = 1

    def check_promotion(self, pos):
        x, y = pos
        if self.board[x][y] == 1:
            if x == 0:
                self.white_kings.append((x, y))
                self.board[x][y] = 3
        elif self.board[x][y] == 2:
            if x == 7:
                self.black_kings.append((x, y))
                self.board[x][y] = 4

    def check_capture(self, pos):
        x, y = pos
        piece = self.board[x][y]
        if piece == 1 or piece == 3:
            if x < 7 and y < 7 and self.board[x+1][y+1] in (2,4):
                if x < 6 and y < 6 and self.board[x+2][y+2] == 0:
                    self.board[x+1][y+1] = 0
                    self.check_capture((x+2, y+2))
            if x < 7 and y > 0 and self.board[x+1][y-1] in (2,4):
                if x < 6 and y > 1 and self.board[x+2][y-2] == 0:
                    self.board[x+1][y-1] = 0
                    self.check_capture((x+2, y-2))
        elif piece == 2 or piece == 4:
            if x > 0 and y < 7 and self.board[x-1][y+1] in (1,3):
                if x > 1 and y < 6 and self.board[x-2][y+2] == 0:
                    self.board[x-1][y+1] = 0
                    self.check_capture((x-2, y+2))
            if x > 0 and y > 0 and self.board[x-1][y-1] in (1,3):
                if x > 1 and y > 1 and self.board[x-2][y-2] == 0:
                    self.board[x-1][y-1] = 0
                    self.check_capture((x-2, y-2))
    def check_for_winner(self):
        white_pieces_left = any(1 in row for row in self.board)
        black_pieces_left = any(2 in row for row in self.board)
        if not white_pieces_left and not black_pieces_left:
            return 0
        elif not white_pieces_left:
            return 2
        elif not black_pieces_left:
            return 1
        else:
            return -1

    def run(self):
        while True:
            if self.turn == 1:
                current_player = self.players[0]
                color = 1
            else:
                current_player = self.players[1]
                color = 2

            current_player.make_move(self, color)
            winner = self.check_for_winner()
            if winner != -1:
                return winner
            self.turn = 3 - self.turn
