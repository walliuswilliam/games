import math, random

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


def create_initial_generation(node_layer_sizes, data, actv_func):
  return [NeuralNet.create_random_nn(node_layer_sizes, data, actv_func) for _ in range(30)]

def create_new_generation(gen):
  sorted_rss = sorted(gen, key=lambda x: x.rss())[:15]
  new_gen = sorted_rss.copy()

  for parent in sorted_rss:
    child_weights = {}
    for pair, weight in parent.weights.items():
      child_weights[pair] = weight+parent.alpha*np.random.normal()
    child_mut_rate = parent.alpha*(math.exp(np.random.normal()/(2**(1/2)*(len(parent.weights))**(1/4))))
    child = NeuralNet(child_weights, parent.data, parent.actv_func, len(parent.neurons), parent.biases, alpha=child_mut_rate, neurons=parent.neurons)
    new_gen.append(child)
  
  return new_gen

def get_avg_rss(gen):
    rss = [net.rss() for net in gen]
    return sum(rss)/len(rss)