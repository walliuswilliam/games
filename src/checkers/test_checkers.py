import sys

sys.path.append('src/checkers')
from checkers import Checkers
from random_player import *


players = [RandomPlayer(), RandomPlayer()]

game = Checkers(players)

# print(game.check_winner())

# game.board = [[0,0,0,0,1,2,0,0],[],[],[],[],[],[],[0,0,0,0,1,2,0,0]]
# game.check_crowns()
n_board = [row.copy() for row in game.board]
n_board[0][0] = 100
print(n_board)
print(game.board)
# print(game.board)
# game.run()
# print(game.winner)
