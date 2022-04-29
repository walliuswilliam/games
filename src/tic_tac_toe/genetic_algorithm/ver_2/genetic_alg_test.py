import sys, os, pkg_resources
pkgs = sorted([str(i.key) for i in pkg_resources.working_set])
if 'matplotlib' not in pkgs: os.system("pip install matplotlib")
sys.path.append('src/tic_tac_toe/')
sys.path.append('src/tic_tac_toe/genetic_algorithm/ver_2')
from dictionary_player import *
from game import *
from genetic_algorithm import *


def vs_first_gen(initial_players, selection_method, fitness_method, population_size, plot=False):
    get_scores(initial_players, fitness_method)
    generations = {0:initial_players}

    get_scores(initial_players, fitness_method, opponents=generations[0][:5])
    gen_scores = [s.mean([p.score for p in generations[0][:5]])]

    for gen_num in range(1, 51):
        print(gen_num)
        generations[gen_num] = create_new_generation(generations[gen_num-1], selection_method, fitness_method, population_size)
        top_players = generations[gen_num][:5]
        get_scores(initial_players, fitness_method, opponents=top_players)
        gen_scores.append(s.mean([p.score for p in top_players]))

    plt.plot(generations.keys(), gen_scores, label=selection_method)
    if plot:
        plt.title(f'{fitness_method} | vs First Gen')
        plt.xlabel('Num Generation')
        plt.ylabel('Avg Score')
        plt.legend()
        plt.savefig(f'src/tic_tac_toe/genetic_algorithm/ver_2/plots/{fitness_method}_vs_first_gen.png')
        plt.clf()

def vs_prev_gen(initial_players, selection_method, fitness_method, population_size, plot=False):
    get_scores(initial_players, fitness_method)
    generations = {0:initial_players}

    get_scores(initial_players, fitness_method, opponents=generations[0][:5])
    gen_scores = [s.mean([p.score for p in generations[0][:5]])]

    for gen_num in range(1, 51):
        print(gen_num)
        generations[gen_num] = create_new_generation(generations[gen_num-1], selection_method, fitness_method, population_size)
        top_players = generations[gen_num][:5]
        get_scores(generations[gen_num-1], fitness_method, opponents=top_players)
        gen_scores.append(s.mean([p.score for p in top_players]))

    plt.plot(generations.keys(), gen_scores, label=selection_method)
    if plot:
        plt.title(f'{fitness_method} | vs Prev Gen')
        plt.xlabel('Num Generation')
        plt.ylabel('Avg Score')
        plt.legend()
        plt.savefig(f'src/tic_tac_toe/genetic_algorithm/ver_2/plots/{fitness_method}_vs_prev_gen.png')
        plt.clf()

def vs_first_and_prev_gen(initial_players, selection_method, fitness_method, population_size, plot=False):
    get_scores(initial_players, fitness_method)
    generations_first = {0:initial_players}
    generations_prev = {0:initial_players}

    get_scores(initial_players, fitness_method, opponents=generations_first[0][:5])
    gen_scores_first = [s.mean([p.score for p in generations_first[0][:5]])]
    gen_scores_prev = [s.mean([p.score for p in generations_prev[0][:5]])]

    for gen_num in range(1, 51):
        print(gen_num)
        generations_first[gen_num] = create_new_generation(generations_first[gen_num-1], selection_method, fitness_method, population_size)
        top_players = generations_first[gen_num][:5]
        get_scores(generations_first[gen_num-1], fitness_method, opponents=top_players)
        gen_scores_first.append(s.mean([p.score for p in top_players]))


        generations_prev[gen_num] = create_new_generation(generations_prev[gen_num-1], selection_method, fitness_method, population_size)
        top_players = generations_prev[gen_num][:5]
        get_scores(initial_players, fitness_method, opponents=top_players)
        gen_scores_prev.append(s.mean([p.score for p in top_players]))
        
    plt.figure(1)
    plt.plot(generations_first.keys(), gen_scores_first, label=selection_method)

    plt.figure(2)
    plt.plot(generations_prev.keys(), gen_scores_prev, label=selection_method)
    if plot:
        plt.figure(1)
        plt.title(f'{fitness_method} | vs First Gen')
        plt.xlabel('Num Generation')
        plt.ylabel('Avg Score')
        plt.legend()
        plt.savefig(f'src/tic_tac_toe/genetic_algorithm/ver_2/plots/{fitness_method}_vs_first_gen.png')

        plt.figure(2)
        plt.title(f'{fitness_method} | vs Prev Gen')
        plt.xlabel('Num Generation')
        plt.ylabel('Avg Score')
        plt.legend()
        plt.savefig(f'src/tic_tac_toe/genetic_algorithm/ver_2/plots/{fitness_method}_vs_prev_gen.png')


first_gen_players = [DictPlayer() for _ in range(64)]


selection_methods = ['hard cutoff', 'stochastic', 'tournament']

for method in selection_methods:
    if method == 'tournament':
        vs_first_and_prev_gen(first_gen_players, method, 'bracket', 32, plot=True)
    else:
        vs_first_and_prev_gen(first_gen_players, method, 'bracket', 32)
