import sys

sys.path.append('src/checkers')
from checkers import Checkers
sys.path.append('src/checkers/players')
from random_player import *
from input_player import *
from neural_net_player import *


# players = [RandomPlayer(), RandomPlayer()]
players = [NeuralNetPlayer(), RandomPlayer()]

# game = Checkers(players)

# game.run(debug=True, symbols=True)
# print(f'Winner: Player {game.winner}')

game = Checkers(players)

board = [[1, 0, 0, 2, 0, -2, -1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, -2],
         [0, 0, 0, 0, 2, 0, 0, 0],
         [0, 0, 0, 0, 0, -1, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]]

print(players[0].convert_board(board))




# board = [[0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0]]