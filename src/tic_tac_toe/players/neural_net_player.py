import sys
sys.path.append('src/tic_tac_toe/fogel')
from fogel_neural_net import *

class NeuralNetPlayer:
    def __init__(self, net=False):
        self.player_num = None
        if net:
            self.net = net
        else:
            self.net = NeuralNet.create_net()

    def set_player_num(self, n):
        self.player_num = n

    def update_board(self, index, value, board):
        board = [i for i in board]
        board[index] = str(value)
        return ''.join(board)

    def choose_space(self, possible_moves, board):
        board = self.convert_board(board)

        assert sum(board) == 0, 'Board sum is not 0'
        for i in set(board): assert i in [-1,0,1], 'Invalid board state'
        
        net_output = self.net.get_net_output(board)
        net_output_tup = [(i,val) for i, val in enumerate(net_output)]
        available_moves = [i for i in net_output_tup if i[0] in possible_moves]
        return max(available_moves, key=lambda item:item[1])[0]

    def convert_board(self, board):
        vec_board = list(board)
        vec_board = [-1 if int(i) == 2 else int(i) for i in vec_board]
        return vec_board


        