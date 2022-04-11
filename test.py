import sys
import os
import pkg_resources
import copy
pkgs = sorted([str(i.key) for i in pkg_resources.working_set])
if 'matplotlib' not in pkgs: os.system("pip install matplotlib")
sys.path.append('src/tic_tac_toe/')
sys.path.append('src/tic_tac_toe/genetic_algorithm/ver_1')
from dictionary_player import *
from game import *
from genetic_algorithm import *

from strat import *

p1, p2 = DictPlayer(strategy=strat_dict), DictPlayer(strategy=strat_dict)

game = Game([p1,p2], starting_player=1)
game.run_to_completion()
print(game.winner)

game = Game([p1,p2], starting_player=2)
game.run_to_completion()
print(game.winner)

quit()

def print_score(gen, retrn=False):
    score = sorted([p.score for p in gen], reverse=True)
    
    if retrn:
        return score
    else:
        print(score)

def avg_score(gen, top=5):
    gen_c = gen.copy()
    gen_c.sort(reverse=True, key=lambda x: x.score)
    gen_c = print_score(gen_c[:top], retrn=True)
    print(s.mean(gen_c))



first_gen = [DictPlayer() for _ in range(25)]
gens = {0:first_gen}


get_scores(first_gen[:5], opponents=first_gen)
print_score(first_gen), avg_score(first_gen)
print('')

for gen_num in range(1,25):
    new_gen = create_new_generation(gens[gen_num-1])
    gens[gen_num] = new_gen
    get_scores(new_gen[:5], opponents=first_gen)
    print_score(new_gen[:5]), avg_score(new_gen)
    print('')

# three_gen = create_new_generation(new_gen)
# get_scores(three_gen[:5], opponents=first_gen)
# print_score(three_gen[:5]), avg_score(three_gen)
# print('')


# four_gen = create_new_generation(three_gen)
# get_scores(four_gen[:5], opponents=first_gen)
# print_score(four_gen[:5]), avg_score(four_gen)
# print('')

# five_gen = create_new_generation(four_gen)
# get_scores(five_gen[:5], opponents=first_gen)
# print_score(five_gen[:5]), avg_score(five_gen)
# print('')

# six_gen = create_new_generation(five_gen)
# get_scores(six_gen[:5], opponents=first_gen)
# print_score(six_gen[:5]), avg_score(six_gen)
# print('')