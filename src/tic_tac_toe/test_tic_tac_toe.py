import sys
sys.path.append('src/tic_tac_toe')
sys.path.append('src/tic_tac_toe/players')
from heuristic_player import *
from random_player import *
from minimax_player import *
from game import *


num_games = 20
num_wins = {1: 0, 2: 0, 'ties': 0}
players = [HeuristicPlayer(2), MinimaxPlayer()]
# players = [HeuristicPlayer(1), HeuristicPlayer(9)]
# players = [MinimaxPlayer(), RandomPlayer()]

for i in range(num_games//2):
    print(i)
    game = Game(players)
    game.run()
    if game.winner != 'Tie':
        num_wins[game.winner] += 1
    else:
        num_wins['ties'] += 1
players.reverse()
for i in range(num_games//2):
    print(i+num_games//2)
    game = Game(players)
    game.run()
    if game.winner != 'Tie':
        num_wins[3-game.winner] += 1
    else:
        num_wins['ties'] += 1

print(num_wins)
