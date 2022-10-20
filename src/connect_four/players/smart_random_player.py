from copy import deepcopy
import random

class SmartRandomPlayer:
    def __init__(self):
        self.player_num = None
        self.invalid_moves = 0
  

    def set_player_num(self, n):
        self.player_num = n

    def choose_move(self, board, possible_moves):
        player_win = False
        opp_win = False
        for space in possible_moves:
            winner = self.check_winner(self.update_board(space, board))
            if winner == self.player_num:
                player_win = space
            elif winner == 3 - self.player_num:
                opp_win = space

        if player_win: return player_win
        if opp_win: return opp_win
        return random.choice(possible_moves)

    def check_winner(self, state):
        #rows
        rows = self.four_in_list(state)
        if rows:
            return rows

        #columns
        cols = self.four_in_list(self.get_cols(state))
        if cols:
            return cols

        #diagonals
        fdiag = [[] for _ in range(len(state) + len(state[0]) - 1)]
        bdiag = [[] for _ in range(len(fdiag))]

        for x in range(len(state[0])):
            for y in range(len(state)):
                fdiag[x + y].append(state[y][x])
                bdiag[x - y - (1 - len(state))].append(state[y][x])

        diag = self.four_in_list(fdiag + bdiag)
        if diag:
            return diag
        
        return False

    def get_cols(self, board):
        cols = []

        for col_idx in range(len(board[0])):
            cols.append([row[col_idx] for row in board])

        return cols

    def update_board(self, move, board):
        board = deepcopy(board)
        cols = self.get_cols(board)
        chosen_col = [*cols[move]]

        col_idx = len(chosen_col)-1 - list(reversed(chosen_col)).index(0)
        board[col_idx][move] = self.player_num
        return board

    def four_in_list(self, lst):
        for string in lst:
            for i in range(0, len(string)-3):
                if string[i] == string[i+1] == string[i+2] == string[i+3] != '0':
                    return string[i]
        return False
