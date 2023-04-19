import sys, random, copy, time

sys.path.append('src/checkers')
sys.path.append('src/checkers/players')
sys.path.append('src/checkers/blondie24')
from checkers import Checkers
from random_player import *
from neural_net_player import *
from neural_net import *
from input_player import *
from tree import Tree


def create_initial_generation(num_nets=30):
    gen = [NeuralNet.create_net(player_num=1, k=2) for _ in range(num_nets)]
    count = 0
    for net in gen:
        count += 1
        print(f'scoring net {count}...')
        temp_gen = gen.copy()
        temp_gen.remove(net)
        opp_nets = random.choices(temp_gen, k=3)
        score_net(net, opp_nets)
        print('done\n')
    return gen

def create_new_generation(gen, parent_net_num=15):
    sorted_nets = sorted(gen, key=lambda x: x.score, reverse=True)[:parent_net_num]
    new_gen = sorted_nets.copy()

    for parent in sorted_nets:
        child = copy.deepcopy(parent)

        for pair, weight in child.weights.items():
            child.weights[pair] = weight+np.random.normal(0, 0.05)
        
        for key, weight in child.weights.items():
            assert parent.weights[key] != weight, 'Weight same as parent'
            assert abs(parent.weights[key] - weight) <= 0.3, 'Weight varies too much'

        if bool(random.getrandbits(1)):
            if bool(random.getrandbits(1)):
                if child.h != 1:
                    deleted_neuron = None
                    while deleted_neuron is None:
                        deleted_neuron = random.choice(child.neurons[2])
                        if deleted_neuron.bias == True:
                            deleted_neuron = None
                    
                    child.h -= 1
                    child.delete_neuron(deleted_neuron)
            else:
                if child.h != 10:
                    child.h += 1
                    child.add_neuron()

        new_gen.append(child)
    
    for child in new_gen: assert 1 <= child.h <= 10, 'Child has invalid number of neurons'


    for net in new_gen:
        temp_gen = new_gen.copy()
        temp_gen.remove(new_gen)
        opp_nets = random.choices(temp_gen, k=5)
        score_net(net, opp_nets)
    return new_gen

def score_net(net, opp_nets):
    score = 0
    count = 0
    for opp in opp_nets:
        s = time.time()
        count+=1
        opp.player_num = 2
        game = Checkers([NeuralNetPlayer(net), NeuralNetPlayer(opp)])
        game.run()
        
        if game.winner == 1:
            score += 1
        elif game.winner == 2:
            score -= 2
        opp.player_num = 1
        print(f'done with game {count} - {round(time.time()-s, 4)} s')
    net.score = score

def best_net_score(gen):
    sorted_nets = sorted(gen, key=lambda x: x.score)
    return sorted_nets[0].score

start = time.time()
initial = create_initial_generation(num_nets=10)
print([i.score for i in initial])
print(f'Time: {time.time()-start}')