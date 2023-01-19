class Checkers:
    def __init__(self, players):
        self.players = players
        self.board = [[(i + j) % 2 * ((3 - ((j < 3) - (j > 4))) % 3) for i in range(8)] for j in range(8)]
        self.turn = 1
        self.set_player_nums()

    def set_player_nums(self):
        for i, player in enumerate(self.players):
            player.player_num = i+1



    def get_pieces(self, player_num):
        valid_pieces = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece == player_num:
                    if piece > 0:
                        
                         or player_num == 3:
                        if j < 7 and self.board[i+1][j+1] == 0:
                            valid_moves.append(((i, j), (i+1, j+1)))
                        if j > 0 and self.board[i+1][j-1] == 0:
                            valid_moves.append(((i, j), (i+1, j-1)))

    def check_winner(self):
        if {i for row in self.board for i in row} == {0}:
            return 'tie'
        elif not any(1 in row for row in self.board):
            return 2
        elif not any(2 in row for row in self.board):
            return 1

    def run_turn():
        for player in players:
            piece = player.choose_piece(self.get_pieces(player))
            translation = player.choose_translation(self.get_translations(piece))

            if piece


    
    def run(self, num_turns=250):
        for i in range(1, 2*num_turns):
            if i % 2 == 0:
                self.turn += 1 
            self.run_turn(self.players[(i % 2) - 1])
            winner = self.check_winner()

            if winner:
                return winner
