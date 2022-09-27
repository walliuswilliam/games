import random, sys
sys.path.append('src/connect_four/tree')
from heuristic_tree import *

class RandomPlayer:
    def __init__(self):
        self.player_num = None
        self.invalid_moves = 0
  

    def set_player_num(self, n):
        self.player_num = n

    def move(self, board):
        return random.choice(self.find_open_spaces(board))

    def find_open_spaces(self, board):
        moves = []
        t_board = [''.join(i) for i in zip(*board)]
        for i, col in enumerate(t_board):
            if '0' in col:
                moves.append(i)
        return moves

class InputPlayer:
    def __init__(self):
        self.player_num = None
        self.invalid_moves = 0
  

    def set_player_num(self, n):
        self.player_num = n

    def move(self, board):
        for row in board:
            print(" ".join(row))
        possible_moves = self.find_open_spaces(board)
        while True:
            move = input(f"Player {self.player_num}'s turn: ")
            if move == 'moves':
                print(possible_moves)
            elif int(move) in possible_moves:
                break
            else:
                print('Invalid move')
        return int(move)

    def find_open_spaces(self, board):
        moves = []
        t_board = [''.join(i) for i in zip(*board)]
        for i, col in enumerate(t_board):
            if '0' in col:
                moves.append(i)
        return moves

class HeuristicPlayer:
    def __init__(self, ply_num):
        self.player_num = None
        self.ply_num = ply_num

    def set_player_num(self, n):
        self.player_num = n
        self.tree = HeuristicTree(self.player_num)
        self.tree.construct_tree(self.tree.root.state, self.ply_num)
        self.tree.set_node_scores()

    def update_board(self, move, board):
        cols = [''.join(i) for i in zip(*board)]
        chosen_col = [*cols[move]]

        col_idx = len(chosen_col)-1 - list(reversed(chosen_col)).index('0')
        row = board[col_idx]
        board[col_idx] = row[:move] + str(self.player_num) + row[move+1:]
        return board

    def move(self, board):
        self.tree.construct_tree(board, self.ply_num)
        self.tree.set_node_scores()
        moves = []
        possible_moves = self.find_open_spaces(board)
        best_move, best_move_idx = self.tree.list_to_string(self.update_board(possible_moves[0], board.copy())), possible_moves[0]

        for move in possible_moves:
            temp_board = self.tree.list_to_string(self.update_board(move, board.copy()))

            if self.tree.states[temp_board].score > self.tree.states[best_move].score:
                best_move, best_move_idx = temp_board, move

        return best_move_idx

    def find_open_spaces(self, board):
        moves = []
        t_board = [''.join(i) for i in zip(*board)]
        for i, col in enumerate(t_board):
            if '0' in col:
                moves.append(i)
        return moves