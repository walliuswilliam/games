import sys
sys.path.append('./src/checkers/blondie24')
from neural_net import *


class NeuralNetPlayer:
    def __init__(self):
        self.player_num = None
        # self.net = NeuralNet()


    def choose_move(self, board, possible_moves):
        pass
        # board = self.convert_board(board)

        # assert sum(board) == 0, 'Board sum is not 0'
        # for i in set(board): assert i in [-1,0,1], 'Invalid board state'
        
        # net_output = self.net.get_net_output(board)
        # net_output_tup = [(i,val) for i, val in enumerate(net_output)]
        # available_moves = [i for i in net_output_tup if i[0] in possible_moves]
        # return max(available_moves, key=lambda item:item[1])[0]

    def convert_board(self, board):
        flattened_board = []
        for row in board:
            for i in row:
                if i > 0:
                    if i == self.player_num:
                        i = 1
                    else:
                        i = -1

                elif i < 0:
                    if abs(i) == self.player_num:
                        i = 'k'
                    else:
                        i = '-k'
            
                flattened_board.append(i)
        return flattened_board
    
    def update_board(self, index, value, board):
        board = [i for i in board]
        board[index] = str(value)
        return ''.join(board)