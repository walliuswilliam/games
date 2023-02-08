import sys
sys.path.append('src/checkers')
sys.path.append('src/checkers/players')
sys.path.append('src/checkers/blondie24')
from checkers import *
from random_player import *
from neural_net_player import *
from neural_net import *

net = NeuralNet.create_net(1)

out = net.get_net_output([[(i + j) % 2 * ((3 - ((j < 3) - (j > 4))) % 3) for i in range(8)] for j in range(8)])

print(out)