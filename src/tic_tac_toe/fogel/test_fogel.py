import os, pkg_resources, sys
pkgs = sorted([str(i.key) for i in pkg_resources.working_set])
if 'numpy' not in pkgs: os.system("pip install numpy")
if 'matplotlib' not in pkgs: os.system("pip install matplotlib")
sys.path.append('src/tic_tac_toe')
sys.path.append('src/tic_tac_toe/players')
sys.path.append('src/tic_tac_toe/fogel')
import matplotlib.pyplot as plt
from game import *
from fogel_neural_net import *
from random_player import *
from neural_net_player import *
from near_perfect_player import *



# game = Game([NeuralNetPlayer(NeuralNet.create_net()), NearPerfectPlayer()])
# game.run()
# print(game.winner)
# quit()


def evolve_neural_net(num_trials, num_gens, print_iter=False):
    trials = {i:[] for i in range(num_trials)} #list full of each generation's best score

    for trial_num in range(num_trials):
        if print_iter: print(f'Trial {trial_num}')
        first_gen = create_initial_generation()
        trials[trial_num].append(best_net_score(first_gen))
        prev_gen = first_gen
        for _ in range(num_gens):
            if print_iter: print(f'\tGen {_}')
            current_gen = create_new_generation(prev_gen)
            trials[trial_num].append(best_net_score(current_gen))
            prev_gen = current_gen
    return trials


def calc_average_scores(trials):
    averages = []
    for gen_num in range(len(trials[0])):
        gen_scores = [list(trials.values())[i][gen_num] for i in range(len(trials.values()))]
        averages.append(sum(gen_scores)/len(gen_scores))

    return averages


# trials = {0: [9, 8, 9, 7, 5, 6, 5, 4, 6, 6, 6], 1: [11, 10, 9, 9, 6, 7, 6, 7, 6, 6, 3], 2: [8, 9, 8, 6, 7, 6, 6, 6, 4, 7, 3]}


trials = evolve_neural_net(3, 50, print_iter=True)
print(trials)
print(calc_average_scores(trials))

x_values = [_ for _ in range(len(trials[0]))]
y_values = list(calc_average_scores(trials))

plt.style.use('bmh')
plt.plot(x_values, y_values)
plt.xlabel('num generations')
plt.ylabel('max total payoff')
plt.savefig('src/tic_tac_toe/fogel/fogel.png')