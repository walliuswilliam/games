import sys
sys.path.append('src/tic_tac_toe')
from dictionary_player import *
from game import *
from itertools import combinations, product


def get_scores(players, opponents=None):
  for player in players:
    player.score = 0
  if opponents != None:
    for player in opponents:
      player.score = 0
    player_combos = product(players, opponents)
    #print([(p1.index, p2.index) for p1,p2 in player_combos])
  else:
    player_combos = combinations(players, 2)
  for combo in player_combos:
    game = Game(combo, starting_player=1)
    game.run_to_completion()
    if type(game.winner) is int:
      game.players[game.winner-1].score += 1
      game.players[(3-game.winner)-1].score -= 1

    game = Game(combo, starting_player=2)
    game.run_to_completion()
    if type(game.winner) is int:
      game.players[game.winner-1].score += 1
      game.players[(3-game.winner)-1].score -= 1
    
    if opponents != None:
      print([(player.index, player.score) for player in combo])

  players.sort(reverse=True, key=lambda x: x.score)
  if opponents != None:
    opponents.sort(reverse=True, key=lambda x: x.score)

def create_new_generation(parents, num_best=5):
  get_scores(parents)
  parents = parents[:num_best]
  parent_combos = combinations(parents, 2)
  children = []
  children_strats = []
  for combo in parent_combos:
    for _ in range (2):
      child = mate(combo)
      children_strats.append(child)
  for strat in children_strats:
    children.append(DictPlayer(strategy=strat))
  get_scores(children)
  return children

def mate(parents): #tuple
  child = {}
  dict1, dict2 = [parent.strategy for parent in parents]
  for items in zip(dict1.items(), dict2.items()):
    child[items[0][0]] = items[random.randint(0,1)][1]
  return child

def run_genetic_algorithm(num_players, num_generations=1):
  players = [DictPlayer() for _ in range(num_players)]
  for generation in range(num_generations):
    players = create_new_generation(players)
  


players = [DictPlayer() for _ in range(25)]
generations = {0:players}

for gen_num in range(1, 51):
  generations[gen_num] = create_new_generation(generations[gen_num-1])


better_players = generations[45][:5]

for index, player in enumerate(players):
  player.index = index

for index, player in enumerate(better_players):
  player.index = index+len(players)

print('players', [player.index for player in players])
print('better players', [player.index for player in better_players])

get_scores(players, better_players)

print([player.score for player in better_players])
