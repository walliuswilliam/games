import sys
sys.path.append('src/connect_four')
from connect_four import *
sys.path.append('src/connect_four/players/competition')
from maia import Row3 as Maia
from justin import *
from charlie import *
from anton import *
from william import *
from cayden import *


num_wins = {1: 0, 2: 0, 'tie': 0}


for _ in range(2):
    print(_)
    players = [Cayden(), William()]
    game = ConnectFour(players)
    game.run()
    num_wins[game.winner] += 1

for _ in range(2):
    print(_+2)
    players = [William(), Cayden()]
    game = ConnectFour(players)
    game.run()

    try: num_wins[3 - game.winner] += 1
    except: num_wins['tie'] += 1

print(num_wins)
