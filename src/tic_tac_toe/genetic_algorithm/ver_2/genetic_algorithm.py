import sys, statistics as s, matplotlib.pyplot as plt
sys.path.append('src/tic_tac_toe')
from dictionary_player import *
from game import *
from itertools import combinations, product


def get_scores(players, fitness_method, opponents=None):
  for player in players:
    player.score = 0
  if opponents != None:
    for opponent in opponents:
      opponent.score = 0
  
  if fitness_method == 'round_robin':  
    if opponents != None:
      player_matchups = product(players, opponents)
    else:
      player_matchups = combinations(players, 2)
    for combo in player_matchups:
      game = Game(combo, starting_player=1)
      game.run()
      if type(game.winner) is int:
        game.players[game.winner-1].score += 1
        game.players[(3-game.winner)-1].score -= 1

      game = Game(combo, starting_player=2)
      game.run()
      if type(game.winner) is int:
        game.players[game.winner-1].score += 1
        game.players[(3-game.winner)-1].score -= 1

  elif fitness_method == 'bracket':
    if opponents != None:
      player_matchups = list(zip(players,opponents))
    else:
      player_matchups = [(players[i],players[i+1]) for i in range(0,len(players)-1,2)]

    while len(player_matchups) > 0:
      next_bracket = []
      for combo in player_matchups:
        game = Game(combo, starting_player=random.randint(1,2))
        game.run()
        if type(game.winner) is int:
          next_bracket.append(combo[game.winner-1])
          combo[game.winner-1].score += 1
        else:
          winner = combo[random.randint(0,1)]
          next_bracket.append(winner)
          winner.score += 1
      player_matchups = [(next_bracket[i],next_bracket[i+1]) for i in range(0,len(next_bracket)-1,2)]

  else:
    raise Exception('Invalid Fitness Method')

def create_new_generation(prev_gen, selection_method, fitness_method, population_size, mutation_rate=0):
  parents = []
  children = []
  if selection_method == 'hard cutoff':
    get_scores(prev_gen, fitness_method)
    parents = sort_by_score(prev_gen)[:population_size//4]
    
    # best = parents[0]
    # win=0
    # lose = 0
    # for p in prev_gen:
    #   best_score = 0
    #   p_score = 0

    #   game = Game([best, p], starting_player=1)
    #   game.run()

    #   if game.winner == 1:
    #     best_score += 1
    #   if game.winner == 2:
    #     p_score += 1
      
    #   game = Game([best, p], starting_player=2)
    #   game.run()

    #   if game.winner == 1:
    #     best_score += 1
    #   if game.winner == 2:
    #     p_score += 1
      
    #   if best_score > p_score:
    #     win += 1
    #   elif p_score > best_score:
    #     lose += 1

    
    # print(f'won {win}/{len(prev_gen)} games')
    # print(f'lost {lose}/{len(prev_gen)} games\n')


  elif selection_method == 'stochastic':
    get_scores(prev_gen, fitness_method)
    
    for i in range(population_size//4):
      possible_parents = [parent for parent in prev_gen if parent not in parents]
      subset = random.choices(possible_parents,k=population_size//8)
      subset = sort_by_score(subset)
      parents.append(subset[0])
    
  elif selection_method == 'tournament':
    for i in range(population_size//4):
      possible_parents = [parent for parent in prev_gen if parent not in parents]
      subset = random.choices(possible_parents,k=population_size//8)
      get_scores(subset, fitness_method)
      subset = sort_by_score(subset)
      parents.append(subset[0])

  else:
    raise Exception('Invalid Selection Method')

  for _ in range(population_size):
    children.append(mate(parents, mutation_rate))

  get_scores(children, fitness_method)
  children = sort_by_score(children)
  return children

def mate(parents_list, mutation_rate): #list
  child_strat = {}
  parents = []
  while len(parents) != 2:
    parent = random.choice(parents_list)
    if parent not in parents:
      parents.append(parent)

  sorted_parents = parents + parents_list #parents 1 and 2 are index 0 and 1, rest of list appended

  parent_chance = (1-mutation_rate)/2
  mutation_choice = random.choices([0,1,random.randint(2,len(sorted_parents)-1)], weights=[parent_chance, parent_chance, mutation_rate])[0]
  
  for key in parent.strategy:
    child_strat[key] = sorted_parents[mutation_choice].strategy[key]
  
  return DictPlayer(strategy=child_strat)

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

