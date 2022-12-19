import random, math

class NearPerfectPlayer:
    def __init__(self):
        self.player_num = None
    
    def set_player_num(self, n):
        self.player_num = n

    def check_winner(self, board):
        rows = [[board[i+3*j] for i in range(3)] for j in range(3)]
        cols = [[board[j+3*i] for i in range(3)] for j in range(3)]
        diags = [[board[i+3*i] for i in range(3)],[board[i+3*(2-i)] for i in range(3)]]
        
        for i in (rows + cols + diags):
            if len(set(i)) == 1 and '0' not in i:
                return int(i[0])
                
        if not any('0' in row for row in board):
            return 'Tie'
    
    def update_board(self, index, value, board):
        board = [i for i in board]
        board[index] = str(value)
        return ''.join(board)

    def choose_space(self, possible_moves, board):        
        if random.randint(1,10) == 1:
            return random.choice(possible_moves)
        
        for move in possible_moves:
            new_board = self.update_board(move, self.player_num, board)
            if self.check_winner(new_board) == self.player_num:
                return move

        for move in possible_moves:
            new_board = self.update_board(move, 3-self.player_num, board)
            if self.check_winner(new_board) == 3-self.player_num:
                return move
        
        rows = [[board[i+3*j] for i in range(3)] for j in range(3)]
        cols = [[board[j+3*i] for i in range(3)] for j in range(3)]
        diags = [[board[i+3*i] for i in range(3)],[board[i+3*(2-i)] for i in range(3)]]

        for i,row in enumerate(rows):
            if row.count('0') == 2 and row.count(str(3-self.player_num)) == 1:
                return i*3+random.choice([n for n,item in enumerate(row) if item == '0'])

        for i,col in enumerate(cols):
            if col.count('0') == 2 and col.count(str(3-self.player_num)) == 1:
                return i+3*random.choice([n for n,item in enumerate(col) if item == '0'])

        for i,diag in enumerate(diags):
            if diag.count('0') == 2 and diag.count(str(3-self.player_num)) == 1:
                choice = random.choice([n for n,item in enumerate(diag) if item == '0'])
                if i == 0:
                    return 4*choice
                else:
                    return 6-2*choice
        
        return random.choice(possible_moves)
