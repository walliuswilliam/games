import math, random, sys, numpy as np
sys.path.append('src/tic_tac_toe')
sys.path.append('src/tic_tac_toe/players')
from game import *
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
    def __init__(self, weights, h):
        self.weights = weights
        self.h = h
        self.biases = [10, 11+self.h]
        
        num_neurons = 20+self.h
        self.neurons = [Neuron(i, lambda x: 1/(1+math.e**(-x))) for i in range(1,num_neurons+1)]
        self.set_node_relations()
        self.score = None

        # self.alpha = alpha #mutation rate

    
    def get_neuron(self, neuron_index):
        return self.neurons[neuron_index-1]

    def clear_net(self):
        for neuron in self.neurons:
            if not neuron.bias:
                neuron.input = None
                neuron.output = None

    def set_node_relations(self):
        for neurons in self.weights.keys():
            neuron_0 = self.get_neuron(neurons[0])
            neuron_1 = self.get_neuron(neurons[1])
            neuron_0.children.append(neuron_1)
            neuron_1.parents.append(neuron_0)
        for neuron in self.neurons:
            if len(neuron.parents) == 0 and neuron.bias == False:
                self.root_neuron = neuron
            if neuron.index <= 10:
                neuron.actv_func = lambda x: x
            if neuron.index in self.biases:
                neuron.bias = True

    def forward_propagate(self, initial_input):
        self.clear_net()
        input_layer = [neuron for neuron in self.neurons if neuron.index < 11]
        for idx, neuron in enumerate(input_layer):
            if neuron.bias:
                continue
            neuron.input = initial_input[idx]
        self.set_bias_outputs()

        queue = [neuron for neuron in input_layer] #self.get_neuron(i) for i in range(11,11+self.h)
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
        return [neuron.output for neuron in self.neurons[-9:]]

    def set_bias_outputs(self):
        for neuron_idx in self.biases:
            neuron = self.get_neuron(neuron_idx)
            neuron.output = 1
    
    def calc_neuron_input(self, neuron):
        total = 0
        for parent in neuron.parents:
            total += self.weights[(parent.index, neuron.index)]*parent.output

        # for weight_nodes in self.weights.keys():
        #     if weight_nodes[1] == neuron.index:
        #         parent = self.get_neuron(weight_nodes[0])
        #         print('neuron', neuron.index, 'parent', neuron.parents, parent.index)
        #         total += self.weights[weight_nodes]*parent.output
        return total

    @classmethod
    def create_net(cls):
        h = random.randint(1,10)
        weights = {}
        biases = [10, 11+h]
        current_node_num = 0
        layers = []
        layer_sizes = [10, h+1, 9]

        for layer_idx, layer_size in enumerate(layer_sizes):
            current_layer = []
            for i in range(layer_size):
                current_node_num += 1
                current_layer.append(current_node_num) 
            layers.append(current_layer)

        for layer_idx, layer in enumerate(layers):
            try:
                next_layer = layers[layer_idx+1]
            except:
                continue
            links = cls.link_layers(layer, next_layer, biases)
            for link in links:
                weights[link] = random.uniform(-0.5,0.5)

        return cls(weights, h)
    
    @classmethod
    def link_layers(cls, layer1, layer2, biases):
        links = []
        for parent in layer1:
            for child in layer2:
                if child not in biases:
                    links.append((parent, child))
        return links


def create_initial_generation():
    gen = [NeuralNet.create_net() for _ in range(50)]
    for net in gen:
        score_net(net)
    return gen

def create_new_generation(gen):
    sorted_nets = sorted(gen, key=lambda x: x.score)[:25]
    new_gen = sorted_nets.copy()

    for parent in sorted_nets:
        child_weights = {}
        for pair, weight in parent.weights.items():
            child_weights[pair] = weight+np.random.normal(0, 0.05)
        child_h = parent.h
        # if bool(random.getrandbits(1)):
        #     if bool(random.getrandbits(1)):
        #         if child_h != 1:
        #             child_h -= 1
        #     else:
        #         if child_h != 10:
        #             child_h += 1
        
        child = NeuralNet(child_weights, child_h)
        new_gen.append(child)
    for net in new_gen:
        score_net(net)
    return new_gen

def score_net(net, num_games=32):
    score = 0
    for i in range(num_games):
        game = Game([NeuralNetPlayer(net), RandomPlayer()])
        game.run()
        if game.winner == 1:
            score +=1
        elif game.winner == 2:
            score -= 0
    net.score = score

def best_net_score(gen):
    sorted_nets = sorted(gen, key=lambda x: x.score)
    return sorted_nets[0].score
