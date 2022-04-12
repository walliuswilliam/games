import sys
import os
import pkg_resources
import copy
pkgs = sorted([str(i.key) for i in pkg_resources.working_set])
if 'matplotlib' not in pkgs: os.system("pip install matplotlib")
sys.path.append('src/tic_tac_toe')
from dictionary_player import *
from game import *
from genetic_algorithm import *

#vs First Gen
first_gen_players = [DictPlayer() for _ in range(25)]
get_scores(first_gen_players)
generations = {0:first_gen_players}

get_scores(first_gen_players, generations[0][:5])
gen_scores = [s.mean([p.score for p in generations[0][:5]])]

for gen_num in range(1, 51):
  generations[gen_num] = create_new_generation(generations[gen_num-1])
  top_players = generations[gen_num][:5]
  get_scores(first_gen_players, top_players)
  gen_scores.append(s.mean([p.score for p in top_players]))

plt.plot(generations.keys(), gen_scores)
plt.title('Avg Score vs First Gen')
plt.xlabel('Num Generation')
plt.ylabel('Avg Score')
plt.savefig('src/tic_tac_toe/genetic_algorithm/ver_1/gen_alg.png')

plt.clf()

#vs Prev Gen
first_gen_players = [DictPlayer() for _ in range(25)]
get_scores(first_gen_players)
generations = {0:first_gen_players}

get_scores(first_gen_players, generations[0][:5])
gen_scores = [s.mean([p.score for p in generations[0][:5]])]

for gen_num in range(1, 51):
  generations[gen_num] = create_new_generation(generations[gen_num-1])
  top_players = generations[gen_num][:5]
  get_scores(generations[gen_num-1], top_players)
  gen_scores.append(s.mean([p.score for p in top_players]))

plt.plot(generations.keys(), gen_scores)
plt.title('Avg Score vs Prev Gen')
plt.xlabel('Num Generation')
plt.ylabel('Avg Score')
plt.savefig('src/tic_tac_toe/genetic_algorithm/ver_1/gen_alg_prev.png')
