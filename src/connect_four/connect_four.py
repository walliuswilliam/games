class ConnectFour:
    def __init__(self, players):
        self.players = players
        self.board = ['0000000' for _ in range(6)]
        for i, player in enumerate(self.players):
            player.player_num = i+1
        self.winner = None

    
    def move(self, player):
        chosen_move = player.move(self.board)
        cols = self.get_cols()
        chosen_col = [*cols[chosen_move]]
        try:
            col_idx = len(chosen_col)-1 - list(reversed(chosen_col)).index('0')
            row = self.board[col_idx]
            self.board[col_idx] = row[:chosen_move] + str(player.player_num) + row[chosen_move+1:]
        except:
            print('Invalid Move')
            player.invalid_moves += 1
            return
        
    def get_cols(self):
        return [''.join(i) for i in zip(*self.board)]

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
        fdiag = ['' for _ in range(len(self.board) + len(self.board[0]) - 1)]
        bdiag = ['' for _ in range(len(fdiag))]

        for x in range(len(self.board[0])):
            for y in range(len(self.board)):
                fdiag[x + y] += self.board[y][x]
                bdiag[x - y - (1 - len(self.board))] += self.board[y][x]

        diag = self.four_in_list(fdiag + bdiag)
        if diag:
            self.winner = diag
        
        if self.winner is None:
            if not any('0' in row for row in self.board):
                self.winner = 'tie'

    def four_in_list(self, lst):
        for string in lst:
            for i in range(4, len(string)):
                if len(set(string[i-4:i])) == 1 and string[i-4] != '0':
                    return string[i-4]
        return False

    def run(self):
        while self.winner is None:
            self.move(self.players[0])
            self.check_winner()
            if self.winner is not None:
                return self.winner
            
            self.move(self.players[1])
            self.check_winner()
            if self.winner is not None:
                return self.winner
        return self.winner
