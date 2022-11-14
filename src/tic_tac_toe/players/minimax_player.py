import sys
sys.path.append('src/tic_tac_toe')
sys.path.append('src/tic_tac_toe/tree')
from game_tree import *
from heuristic_tree import *

class MinimaxPlayer:
    def __init__(self):
        self.player_num = None

    def set_player_num(self, n):
        self.player_num = n
        self.tree = GameTree(self.player_num)
        self.tree.construct_tree()
        self.tree.set_node_scores()

    def update_board(self, index, value, board):
        board = [i for i in board]
        board[index] = str(value)
        return ''.join(board)

    def choose_space(self, possible_moves, board):
        moves = []
        best_move, best_move_idx = self.update_board(possible_moves[0], self.player_num, board), possible_moves[0]

        for move in possible_moves:
            temp_board = self.update_board(move, self.player_num, board)
            if self.tree.states[temp_board].score > self.tree.states[best_move].score:
                best_move, best_move_idx = temp_board, move

        return best_move_idx