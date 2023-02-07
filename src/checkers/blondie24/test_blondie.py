import sys
sys.path.append('src/checkers')
sys.path.append('src/checkers/players')
sys.path.append('src/checkers/blondie24')
from checkers import *
from random_player import *
from neural_net_player import *
from neural_net import *

net = NeuralNet.create_net()
print(net.weights.keys())
print(len(net.weights))

print([len(i) for i in net.neurons.values()])