import sys
sys.path.append('src/tic_tac_toe')
from players import *
from game import *

num_wins = {1: 0, 2: 0, 'ties': 0}
players = [MinimaxPlayer(), RandomPlayer()]

count = 0
while count < 100:
  if count%2 == 0:
    game = Game(players)
    game.run_to_completion()
    if game.winner != 'Tie':
      num_wins[game.winner] += 1
    else:
      num_wins['ties'] += 1
  else:
    players.reverse()
    game = Game(players)
    game.run_to_completion()
    if game.winner != 'Tie':
      num_wins[3-game.winner] += 1
    else:
      num_wins['ties'] += 1
    players.reverse()
  count += 1
  print(count)

print(num_wins)
