import random

class Checkers:
    def __init__(self, players):
        self.players = players
        self.board = [[(i + j) % 2 * ((3 - ((j < 3) - (j > 4))) % 3) for i in range(8)] for j in range(8)]
        self.turn = 1
        self.winner = None
        self.set_player_nums()


    def set_player_nums(self):
        for i, player in enumerate(self.players):
            player.player_num = i+1

    def get_moves(self, player_num, board=None):
        if board == None:
            board = self.board
        valid_moves = []
        for i in range(8):
            for j in range(8):
                piece_num = board[i][j]

                if abs(piece_num) == player_num:
                    if piece_num == 1 or piece_num < 0:
                            try:
                                if i>0 and j>0 and board[i-1][j-1] == 0:
                                    valid_moves.append(((i, j), (-1, -1)))
                                elif i>0 and j>0 and board[i-1][j-1] == 3-player_num and board[i-2][j-2] == 0:
                                    valid_moves.append(((i, j), (-2, -2)))
                            except: pass
                            try:
                                if i>0 and board[i-1][j+1] == 0:
                                    valid_moves.append(((i, j), (-1, 1)))
                                elif i>0 and board[i-1][j+1] == 3-player_num and board[i-2][j+2] == 0:
                                    valid_moves.append(((i, j), (-2, 2)))
                            except: pass
                    
                    if piece_num == 2 or piece_num < 0:
                            try:
                                if board[i+1][j+1] == 0:
                                    valid_moves.append(((i, j), (1, 1)))
                                elif board[i+1][j+1] == 3-player_num and board[i+2][j+2] == 0:
                                    valid_moves.append(((i, j), (2, 2)))
                                    
                            except: pass
                            try:
                                if j>0 and board[i+1][j-1] == 0:
                                    valid_moves.append(((i, j), (1, -1)))
                                elif j>0 and board[i+1][j-1] == 3-player_num and board[i+2][j-2] == 0:
                                    valid_moves.append(((i, j), (2, -2)))
                            except: pass
        return valid_moves
    
    def check_crowns(self):
        for idx in range(len(self.board[0])):
            if self.board[0][idx] == 1:
                self.board[0][idx] = -1
        for idx in range(len(self.board[-1])):
            if self.board[-1][idx] == 2:
                self.board[-1][idx] = -2

    def apply_translation(self, move):
        return (move[0][0] + move[1][0], move[0][1] + move[1][1])

    @staticmethod
    def check_winner(self):
        if {i for row in self.board for i in row} == {0}:
            return 'tie'
        elif not any(1 in row for row in self.board) and not any(-1 in row for row in self.board):
            return 2
        
        elif not any(2 in row for row in self.board) and not any(-2 in row for row in self.board):
            return 1

    def run_turn(self, player, piece=None, debug=False, symbols=False):
        if debug: self.print_board(symbols=symbols)
        possible_moves = self.get_moves(player.player_num)

        if piece:
            temp_moves = []
            for move in possible_moves:
                if move[0] == piece:
                    if 2 in move[1] or -2 in move[1]:
                        temp_moves.append(move)
            if len(temp_moves) == 0:
                return
            else:
                temp_moves.append((piece, (0,0)))
            possible_moves = temp_moves
            
        if len(possible_moves) == 0:
            self.winner = 3-player.player_num
            return
        move = player.choose_move([row.copy() for row in self.board], possible_moves)
        if move not in possible_moves:
            print('Invalid Move')
            move = random.choice(possible_moves)
        if move[1] == (0,0):
            return

        if debug: print('Move:', move)
        new_move = self.apply_translation(move)
        self.board[new_move[0]][new_move[1]] = self.board[move[0][0]][move[0][1]]
        self.board[move[0][0]][move[0][1]] = 0
        self.check_crowns()
        if 2 in move[1] or -2 in move[1]:
            self.board[move[0][0] + move[1][0]//2][move[0][1] + move[1][1]//2] = 0
            self.run_turn(player, piece=new_move, debug=debug, symbols=symbols)

    def run(self, num_turns=250, debug=False, symbols=False):
        for i in range(1, 2*num_turns):
            if i % 2 == 0:
                self.turn += 1 
            self.run_turn(self.players[(i % 2) - 1], debug=debug, symbols=symbols)
            if not self.winner:
                self.winner = self.check_winner()
            if debug:
                print(f'\nPlayer {self.players[(i % 2)].player_num} turn') 
            if self.winner:
                return self.winner
    
    def print_board(self, board=None, symbols=False):
        if not board:
            board = self.board
        if symbols:
            print('   ', *range(8), '\n    ―――――――――――――――')
            for i, row in enumerate(board):
                symbols = {-1:'♚', 1:'⬤', -2:'♔', 2:'◯', 0:'⬚'}
                row = [symbols[i] for i in row]
                print(i, '|', *row, sep=' ')

        else:
            print('   ', *range(8), '\n    ―――――――――――――――')
            for i, row in enumerate(board):
                print(i, '|', *row, sep=' ')
