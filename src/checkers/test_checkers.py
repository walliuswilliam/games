import sys

sys.path.append('src/checkers')
from checkers import Checkers
from random_player import *


players = [RandomPlayer(), RandomPlayer()]

game = Checkers(players)
game.print_board()
game.get_moves(1)

# print(game.check_winner())

# game.board = [[0,0,0,0,1,2,0,0],[],[],[],[],[],[],[0,0,0,0,1,2,0,0]]
# game.check_crowns()
# n_board = [row.copy() for row in game.board]
# n_board[0][0] = 100
# print(n_board)
# print(game.board)
# print(game.board)
# game.run()
# print(game.winner)
