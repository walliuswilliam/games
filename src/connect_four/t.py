import sys
sys.path.append('src/connect_four')
sys.path.append('src/connect_four/players')
from connect_four import *
from competition_player import *


players = [CompPlayer(6), CompPlayer(6)]

game = ConnectFour(players)
game.run(print_game=True)
print(game.winner)
quit()