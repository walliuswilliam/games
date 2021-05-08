import sys
sys.path.append('src/tic_tac_toe')
from player import *
from game import *


num_wins = {1: 0, 2: 0, 'ties': 0}
for _ in range(200):
  players = [Player(), Player()]
  game = Game(players, starting_player=(((_+1)%2)+1))
  game.run_to_completion()
  if game.winner != 'Tie':
    num_wins[game.winner] += 1
  else:
    num_wins['ties'] += 1

print(num_wins)