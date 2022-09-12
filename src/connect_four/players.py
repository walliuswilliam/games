import random, sys
sys.path.append('src/tic_tac_toe/tree')
from game_tree import *

class RandomPlayer:
    def __init__(self):
        self.player_num = None
        self.invalid_moves = 0
  

    def move(self, board):
        return random.choice(self.find_open_spaces(board))

    def find_open_spaces(self, board):
        moves = []
        t_board = [''.join(i) for i in zip(*board)]
        for i, col in enumerate(t_board):
            if '0' in col:
                moves.append(i)
        return moves


