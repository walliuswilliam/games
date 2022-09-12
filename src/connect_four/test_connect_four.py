import sys
sys.path.append('src/connect_four')
from players import *
from connect_four import *


players = [RandomPlayer(), RandomPlayer()]
game = ConnectFour(players)

game.run()
print(game.winner)
