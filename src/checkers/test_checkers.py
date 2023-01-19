import sys

sys.path.append('src/checkers')
from checkers import *
from random_player import *


players = [RandomPlayer(), RandomPlayer()]

game = Checkers(players)

print(game.check_winner())
# print(game.board)
# game.run()
# print(game.winner)
