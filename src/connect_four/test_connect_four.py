import sys
sys.path.append('src/connect_four')
from players import *
from connect_four import *


players = [InputPlayer(), RandomPlayer()]
game = ConnectFour(players)

game.run()
print(f'Winner: Player {game.winner}')
