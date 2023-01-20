import random

class Checkers:
    def __init__(self, players):
        self.players = players
        self.board = [[(i + j) % 2 * ((3 - ((j < 3) - (j > 4))) % 3) for i in range(8)] for j in range(8)]
        self.turn = 1
        self.set_player_nums()

    def set_player_nums(self):
        for i, player in enumerate(self.players):
            player.player_num = i+1

    def get_moves(self, player_num):
        valid_moves = []
        for i in range(8):
            for j in range(8):
                piece_num = self.board[i][j]

                if piece_num == player_num:
                    if piece_num == 1 or piece_num < 0:
                            try: #[-1] is valid, need to fix
                                if i>0 and j>0 and self.board[i-1][j-1] == 0:
                                    valid_moves.append(((i, j), (-1, -1)))
                            except: pass
                            try:
                                if i>0 and self.board[i-1][j+1] == 0:
                                    valid_moves.append(((i, j), (-1, 1)))
                            except: pass
                    
                    if piece_num == 2 or piece_num < 0:
                            try:
                                if self.board[i+1][j+1] == 0:
                                    valid_moves.append(((i, j), (1, 1)))
                            except: pass
                            try:
                                if j>0 and self.board[i+1][j-1] == 0:
                                    valid_moves.append(((i, j), (1, -1)))
                            except: pass
        print(valid_moves)

                        
                        

                        
                #          or player_num == 3:
                #         if j < 7 and self.board[i+1][j+1] == 0:
                #             valid_moves.append(((i, j), (i+1, j+1)))
                #         if j > 0 and self.board[i+1][j-1] == 0:
                #             valid_moves.append(((i, j), (i+1, j-1)))
    
    def check_crowns(self):
        for idx in range(len(self.board[0])):
            if self.board[0][idx] == 1:
                self.board[0][idx] = -1
        for idx in range(len(self.board[-1])):
            if self.board[-1][idx] == 2:
                self.board[-1][idx] = -2

    def check_winner(self):
        if {i for row in self.board for i in row} == {0}:
            return 'tie'
        elif not any(1 in row for row in self.board):
            return 2
        elif not any(2 in row for row in self.board):
            return 1

    def run_turn(self, player):
        possible_moves = self.get_moves(player)
        move = player.choose_move([row.copy() for row in self.board], possible_moves)
        if move not in possible_moves:
            print('Invalid Move')
            move = random.choice(possible_moves)
        
        self.board[move[0][0]][move[0][1]] = 0
        self.board[move[0][0] + move[1][0]][move[0][1] + move[1][1]] = player.player_num


    
    def run(self, num_turns=250):
        for i in range(1, 2*num_turns):
            if i % 2 == 0:
                self.turn += 1 
            self.run_turn(self.players[(i % 2) - 1])
            winner = self.check_winner()

            if winner:
                return winner
    
    def print_board(self, board=None):
        if not board:
            board = self.board
        print('   ', *range(8), '\n    ―――――――――')
        for i, row in enumerate(board):
            print(i, '|', *row, sep=' ')
    

