import math, random, sys, numpy as np, copy
sys.path.append('src/tic_tac_toe')
sys.path.append('src/tic_tac_toe/players')
from game import *
from random_player import *
from neural_net_player import *
from near_perfect_player import *
from logger import *


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
    def __init__(self, neurons, weights, h):
        self.neurons = neurons # {1:[node_obj, ...], 2:[], 3:[]}
        self.weights = weights
        self.h = h
        self.biases = [10, 11+self.h]
        
        self.set_node_relations()
        self.score = None

    
    def get_neuron(self, neuron_index):
        for layer in self.neurons.values():
            for neuron in layer:
                if neuron.index == neuron_index:
                    return neuron

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
                if neuron.index <= 10:
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
            if curr_neuron.index not in range(11) and curr_neuron.bias == False:
                curr_neuron.input = self.calc_neuron_input(curr_neuron)
            curr_neuron.update_output()

            visited.append(curr_neuron.index)
            for child in curr_neuron.children:
                if child.index not in visited and child.index not in [n.index for n in queue]:
                    queue.append(child)
            queue.pop(0)
        
    def get_net_output(self, initial_input):
        self.forward_propagate(initial_input)
        return [neuron.output for neuron in self.neurons[3]]

    def set_bias_outputs(self):
        for neuron_idx in self.biases:
            neuron = self.get_neuron(neuron_idx)
            neuron.output = 1
    
    def calc_neuron_input(self, neuron):
        total = 0
        for parent in neuron.parents:
            total += self.weights[(parent.index, neuron.index)]*parent.output

        return total
    
    def delete_neuron(self, neuron):
        new_weights = {}
        for weight, value in self.weights.items():
            if neuron.index not in weight:
                new_weights[weight] = value

        self.weights = new_weights
        for layer in self.neurons.values():
            try:
                layer.remove(neuron)
            except:
                continue
            
        for existing_neuron in self.neurons[1]+self.neurons[3]:
            if neuron in existing_neuron.parents:
                existing_neuron.parents.remove(neuron)
            if neuron in existing_neuron.children:
                existing_neuron.children.remove(neuron)

    def add_neuron(self):
        new_weights = {}
        
        max_neuron = self.neurons[1][0]
        for layer in self.neurons.values():
            for neuron in layer:
                if neuron.index > max_neuron.index:
                    max_neuron = neuron
        new_neuron = Neuron(max_neuron.index+1, lambda x: 1/(1+math.e**(-x)))
        self.neurons[2].append(new_neuron)

        for neuron in self.neurons[1]:
            new_neuron.parents.append(neuron)
            neuron.children.append(new_neuron)
            new_weights[(neuron.index, new_neuron.index)] = 0
        
        for neuron in self.neurons[3]:
            neuron.parents.append(new_neuron)
            new_neuron.children.append(neuron)
            new_weights[(new_neuron.index, neuron.index)] = 0
        self.weights.update(new_weights)


    @classmethod
    def create_net(cls):
        h = random.randint(1,10)
        weights = {}
        neurons = {1:[], 2:[], 3:[]}
        biases = [10, 11+h]
        current_node_num = 0
        layers = []
        layer_sizes = [10, h+1, 9]

        for layer_idx, layer_size in enumerate(layer_sizes):
            for i in range(layer_size):
                current_node_num += 1
                neurons[layer_idx+1].append(Neuron(current_node_num, lambda x: 1/(1+math.e**(-x))))

        weight_relations = cls.create_weight_relations(neurons[1], neurons[2], biases)
        weight_relations += cls.create_weight_relations(neurons[2], neurons[3], biases)
        for weight in weight_relations:
            weights[weight] = random.uniform(-0.5,0.5)

        return cls(neurons, weights, h)
    
    @classmethod
    def create_weight_relations(cls, layer1, layer2, biases):
        links = []
        for parent in layer1:
            for child in layer2:
                if child not in biases:
                    links.append((parent.index, child.index))
        return links


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
