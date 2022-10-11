import sys
sys.path.append('src/connect_four')
from players import *
from connect_four import *


num_games = 100
num_wins = {1: 0, 2: 0, 'ties': 0}
players = [HeuristicPlayer(3), SmartRandomPlayer()]

# game = ConnectFour(players)
# game.run()
# print(game.winner)
# quit()

for i in range(num_games//2):
    # print(i)
    game = ConnectFour(players)
    game.run()
    if game.winner != 'tie':
        num_wins[game.winner] += 1
    else:
        num_wins['ties'] += 1
players.reverse()
for i in range(num_games//2):
    # print(i+num_games//2)
    game = ConnectFour(players)
    game.run()
    if game.winner != 'tie':
        num_wins[3-game.winner] += 1
    else:
        num_wins['ties'] += 1

print(num_wins)
