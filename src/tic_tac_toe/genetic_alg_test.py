import sys
sys.path.append('src/tic_tac_toe')
from dictionary_player import *
from game import *
from itertools import combinations














all_players = [DictPlayer(_) for _ in range(25)]
all_game_players = combinations(all_players, 2)

for player_combo in all_game_players:
  game = Game(player_combo, starting_player=1)
  game.run_to_completion()
  if type(game.winner) is int:
    game.players[game.winner-1].score += 1
    game.players[(3-game.winner)-1].score -= 1

  game = Game(player_combo, starting_player=2)
  game.run_to_completion()
  if type(game.winner) is int:
    game.players[game.winner-1].score += 1
    game.players[(3-game.winner)-1].score -= 1

all_players.sort(reverse=True, key=lambda x: x.score)
all_players = all_players[:5]


second_gen_parents = list(combinations(all_players, 2))


def mate(parents): #tuple
  child = {}
  dict1, dict2 = [parent.strategy for parent in parents]
  for items in zip(dict1.items(), dict2.items()):
    child[items[0][0]] = items[random.randint(0,1)][1]
  return child


second_gen = []
for combo in second_gen_parents:
  for _ in range (2):
    child = mate(combo)
    second_gen.append(child)





# game.complete_turn(3-game.starting_player)
# game.check_winner()
# print(game.winner)





# num_wins = {1: 0, 2: 0, 'ties': 0}
# for _ in range(200):
#   players = [DictPlayer(), DictPlayer()]
#   game = Game(players, starting_player=(((_+1)%2)+1))
#   game.run_to_completion()
#   if game.winner != 'Tie':
#     num_wins[game.winner] += 1
#   else:
#     num_wins['ties'] += 1

# print(num_wins)