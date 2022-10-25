import sys
from copy import deepcopy
sys.path.append('src/connect_four/tree')
from heuristic_tree import *

class HeuristicPlayer:
    def __init__(self, ply_num):
        self.number = None
        self.ply_num = ply_num


    def set_player_number(self, n):
        self.number = n
        self.tree = HeuristicTree(self.player_num)
        self.tree.construct_tree(self.tree.root.state, self.ply_num)
        self.tree.set_node_scores()

    def update_board(self, move, board):
        board = deepcopy(board)
        cols = self.get_cols(board)
        chosen_col = [*cols[move]]

        col_idx = len(chosen_col)-1 - list(reversed(chosen_col)).index(0)
        board[col_idx][move] = self.player_num
        return board

    def get_cols(self, board):
        cols = []

        for col_idx in range(len(board[0])):
            cols.append([row[col_idx] for row in board])

        return cols
    
    def convert_board(self, board):
        board = [[str(i) for i in row] for row in deepcopy(board)]
        new_board = []
        for row in board:
            new_board.append(''.join(row))
        return new_board

    def choose_move(self, board, possible_moves):    
        self.tree.construct_tree(self.convert_board(board.copy()), self.ply_num)
        self.tree.set_node_scores()
        best_move, best_move_idx = self.tree.list_to_string(self.convert_board(self.update_board(possible_moves[0], board))), possible_moves[0]

        for move in possible_moves:
            temp_board = self.tree.list_to_string(self.convert_board(self.update_board(move, board)))

            if self.tree.states[temp_board].score > self.tree.states[best_move].score:
                best_move, best_move_idx = temp_board, move

        return best_move_idx
