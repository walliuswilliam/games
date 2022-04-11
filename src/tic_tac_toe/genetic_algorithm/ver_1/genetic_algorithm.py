import sys
sys.path.append('src/tic_tac_toe')
from dictionary_player import *
from game import *
from itertools import combinations, product
import matplotlib.pyplot as plt
import statistics as s


def get_scores(players, opponents=None):
  for player in players:
    player.score = 0
  if opponents != None:
    for opponent in opponents:
      opponent.score = 0
    player_combos = product(players, opponents)
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

def create_new_generation(parents, num_best=5):
  get_scores(parents)
  parents = sort_by_score(parents)[:num_best]
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
  children = sort_by_score(children)
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
  
def sort_by_score(players):
  players.sort(reverse=True, key=lambda x: x.score)
  return players

def validate_generation(generation): #list of players
  gen_scores = [p.score for p in generation]
  if gen_scores[0] < 0 or gen_scores[-1] > 0:
    raise Exception(f'Invalid Scores: {gen_scores}')
  
  for i in range(len(gen_scores)):
    if i == 0:
      continue
    if gen_scores[i] > gen_scores[i-1]:
      raise Exception(f'Misordered Scores: {gen_scores}')
