import sys
sys.path.append('src/tic_tac_toe/fogel')
from fogel_neural_net import *

class NeuralNetPlayer:
    def __init__(self, weights):
        self.player_num = None
        self.net = NeuralNet(weights)

    def set_player_num(self, n):
        self.player_num = n

    def update_board(self, index, value, board):
        board = [i for i in board]
        board[index] = str(value)
        return ''.join(board)

    def choose_space(self, possible_moves, board):
        self.convert_board(board)

    def convert_board(self, board):
        vec_board = list(board)
        vec_board = [-1 if int(i) == 2 else int(i) for i in vec_board]
        print(vec_board)


        