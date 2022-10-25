from copy import deepcopy

class ConnectFour:
    def __init__(self, players):
        self.players = players
        self.board = [[0 for i in range(7)] for j in range(6)]
        for i, player in enumerate(self.players):
            player.set_player_number(i+1)
        self.winner = None

    
    def move(self, player):
        chosen_move = player.choose_move(deepcopy(self.board), self.find_open_spaces(self.board))
        cols = self.get_cols()
        chosen_col = [*cols[chosen_move]]


        # self.print_board()
        # print(chosen_move)
        # print(player.number)
        # print(col_idx)
        # print(self.board[col_idx][chosen_move])
        

        try:
            # print(list(reversed(chosen_col)))
            col_idx = len(chosen_col)-1 - list(reversed(chosen_col)).index(0)
            self.board[col_idx][chosen_move] = player.number

        except:
            print('Invalid Move')
            return self.find_open_spaces(self.board)[0]
        # print()

    def find_open_spaces(self, board):
        moves = []
        for i, col in enumerate(self.get_cols(board=board)):
            if 0 in col:
                moves.append(i)
        return moves
        
    def get_cols(self, board=False):
        if not board:
            board = self.board
        cols = []

        for col_idx in range(len(board[0])):
            cols.append([row[col_idx] for row in board])

        return cols

    def check_winner(self):
        #rows
        rows = self.four_in_list(self.board)
        if rows:
            self.winner = rows

        #columns
        cols = self.four_in_list(self.get_cols())
        if cols:
            self.winner = cols

        #diagonals
        fdiag = [[] for _ in range(len(self.board) + len(self.board[0]) - 1)]
        bdiag = [[] for _ in range(len(fdiag))]

        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                fdiag[x + y].append(self.board[y][x])
                bdiag[x - y - (1 - len(self.board))].append(self.board[y][x])

        diag = self.four_in_list(fdiag + bdiag)
        if diag:
            self.winner = diag
        
        if self.winner is None:
            if not any(0 in row for row in self.board):
                self.winner = 'tie'

    def four_in_list(self, lst):
        for sub_lst in lst:
            for i in range(0, len(sub_lst)-3):
                if sub_lst[i] == sub_lst[i+1] == sub_lst[i+2] == sub_lst[i+3] != 0:
                    return sub_lst[i]
        return False
    
    def print_board(self):
        board = self.board.copy()
        board = [[str(i) for i in board[j]] for j in range(len(board))]
        
        for line in board:
            print(' '.join(line))

    def run(self, print_game=False):
        while self.winner is None:
            self.move(self.players[0])
            if print_game: self.print_board(), print()
            self.check_winner()
            if self.winner is not None:
                return self.winner
            
            self.move(self.players[1])
            if print_game: self.print_board(), print()
            self.check_winner()
            if self.winner is not None:
                return self.winner
        return self.winner
