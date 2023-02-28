import math, random, sys, numpy as np, copy
sys.path.append('src/checkers')
sys.path.append('src/checkers/players')
from checkers import *
from random_player import *
from neural_net_player import *


class Neuron:
    def __init__(self, idx, actv_func, bias=False):
        self.index = idx
        self.bias = bias
        self.actv_func = actv_func
        self.input = None
        self.output = 1 if bias else None
        self.children = []
        self.parents = []

    def update_output(self):
        if self.bias:
            self.output = 1
        else:
            self.output = self.actv_func(self.input)

class NeuralNet:
    def __init__(self, neurons, weights, player_num):
        self.neurons = neurons # {1:[node_obj, ...], ..., 4:[]}
        self.weights = weights
        self.biases = [33, 74, 85]
        self.player_num = player_num
        
        self.set_node_relations()
        self.score = None

    
    def get_neuron(self, neuron_index):
        for layer in self.neurons.values():
            for neuron in layer:
                if neuron.index == neuron_index:
                    return neuron

    def get_flat_neuron_list(self):
        return [i for j in self.neurons.values() for i in j]

    def clear_net(self):
        for layer in self.neurons.values():
            for neuron in layer:
                if not neuron.bias:
                    neuron.input = None
                    neuron.output = None

    def set_node_relations(self):
        for layer in self.neurons.values():
            for neuron in layer:
                neuron.parents = []
                neuron.children = []
        for neurons in self.weights.keys():
            neuron_0 = self.get_neuron(neurons[0])
            neuron_1 = self.get_neuron(neurons[1])

            neuron_0.children.append(neuron_1)
            neuron_1.parents.append(neuron_0)
        for layer in self.neurons.values():
            for neuron in layer:
                if neuron.index <= 32:
                    neuron.actv_func = lambda x: x
                if neuron.index in self.biases:
                    neuron.bias = True

    def forward_propagate(self, initial_input):
        self.clear_net()

        for idx, neuron in enumerate(self.neurons[1]):
            if neuron.bias:
                continue
            neuron.input = initial_input[idx]
        self.set_bias_outputs()

        queue = [neuron for neuron in self.neurons[1]]
        visited = []
        while queue != []:
            curr_neuron = queue[0]
            # print(curr_neuron.index, [i.index for i in curr_neuron.parents])

            if curr_neuron == self.get_flat_neuron_list()[-1]:              
                if len(self.get_flat_neuron_list()) >= 87:
                    neuron = self.get_neuron(87)
                    neuron.output = sum([i.input for i in self.neurons[1] if i.bias == False])
                else:
                    idx = len(self.get_flat_neuron_list())+1
                    weight = (idx, curr_neuron.index)

                    if weight not in self.weights:
                        self.weights[weight] = random.uniform(-0.2,0.2)
                    neuron = Neuron(idx, lambda x: x)
                    neuron.output = sum([i.input for i in self.neurons[1] if i.bias == False])
                    # print()

                    # print(self.get_neuron(87).index)
                    
                    self.neurons[len(self.neurons)-1].append(neuron)
                    curr_neuron.parents.append(neuron)

            if curr_neuron.index not in range(len(self.neurons[1])) and curr_neuron.bias == False and curr_neuron.index != 87:
                curr_neuron.input = self.calc_neuron_input(curr_neuron)
            curr_neuron.update_output()

            visited.append(curr_neuron.index)
            for child in curr_neuron.children:
                if child.index not in visited and child.index not in [n.index for n in queue]:
                    queue.append(child)
            queue.pop(0)
        
    def get_net_output(self, initial_input):
        board = self.convert_board(initial_input)
        self.forward_propagate(board)
        return self.neurons[4][0].output

    def set_bias_outputs(self):
        for neuron_idx in self.biases:
            neuron = self.get_neuron(neuron_idx)
            neuron.output = 1
    
    def calc_neuron_input(self, neuron):
        total = 0
        # print(self.weights.keys())
        # quit()
        for parent in neuron.parents:
            # print((parent.index, neuron.index), parent.output)
            total += self.weights[(parent.index, neuron.index)]*parent.output
        return total
    


    @classmethod
    def create_net(cls, player_num):
        weights = {}
        neurons = {1:[], 2:[], 3:[], 4:[]}
        biases = [33, 74, 85]

        current_node_num = 0
        layer_sizes = [33, 41, 11, 1]

        for layer_idx, layer_size in enumerate(layer_sizes):
            for _ in range(layer_size):
                current_node_num += 1
                neurons[layer_idx+1].append(Neuron(current_node_num, lambda x: math.tanh(x)))

        # print(neurons[4][0].index)
        # quit()
        weight_relations = []
        for i,j in zip(range(1, len(neurons)), range(2, len(neurons)+1)):
            # print(i,j)
            # print(cls.create_weight_relations(neurons[i], neurons[j], biases))
            weight_relations += cls.create_weight_relations(neurons[i], neurons[j], biases)


        for weight in weight_relations:
            weights[weight] = random.uniform(-0.2,0.2)
        # print(weights)
        # quit()
        return cls(neurons, weights, player_num)
    
    @classmethod
    def create_weight_relations(cls, layer1, layer2, biases):
        links = []
        for parent in layer1:
            for child in layer2:
                if child.index not in biases:
                    links.append((parent.index, child.index))
        return links
    
    def convert_board(self, board):
        flattened_board = []
        index = 0

        for row_idx, row in enumerate(board):
            for i in row:
                if i > 0:
                    if i == self.player_num:
                        i = 1
                    else:
                        i = -1

                elif i < 0:
                    if abs(i) == self.player_num:
                        i = 'k'
                    else:
                        i = '-k'
                if row_idx%2 == 0:
                    if index%2 == 1:
                        flattened_board.append(i)
                else:
                    if index%2 == 0:
                        flattened_board.append(i)
                index += 1
        return flattened_board


def create_initial_generation():
    gen = [NeuralNet.create_net() for _ in range(50)]
    for net in gen:
        score_net(net)
    return gen

def create_new_generation(gen):
    sorted_nets = sorted(gen, key=lambda x: x.score, reverse=True)[:25]
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

    h = [child.h for child in new_gen]
    assert len(set(h)) != 1, 'Consistant h values'

    for net in new_gen:
        score_net(net)
    return new_gen

def score_net(net, num_games=32):
    score = 0
    for i in range(num_games):
        game = Game([NeuralNetPlayer(net), NearPerfectPlayer()])
        game.run()
        
        if game.winner == 1:
            score += 1
        elif game.winner == 2:
            score -= 10
        
    net.score = score

def best_net_score(gen):
    sorted_nets = sorted(gen, key=lambda x: x.score)
    return sorted_nets[0].score
