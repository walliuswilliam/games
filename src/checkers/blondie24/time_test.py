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


s = time.time()
nn1 = NeuralNet.create_net(player_num=1, k=2)
nn2 = NeuralNet.create_net(player_num=2, k=2)


for key in nn1.weights:
    nn1.weights[key] = 0.1

for key in nn2.weights:
    nn2.weights[key] = 0.1


# nn1.get_net_output([[1, 0, 0, 2, 0, -2, -1, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, -2],
#          [0, 0, 0, 0, 2, 0, 0, 0],
#          [0, 0, 0, 0, 0, -1, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0],
#          [0, 0, 1, 0, 0, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 0, 0]])
# print(f'Time: {time.time()-s} s')
# quit()
game = Checkers([NeuralNetPlayer(nn1), NeuralNetPlayer(nn2)])
# game = Checkers([RandomPlayer(), RandomPlayer()])
game.run()

print('Winner', game.winner)
print(f'Time: {time.time()-s} s')