import sys
sys.path.append('src/tic_tac_toe')
sys.path.append('src/tic_tac_toe/players')
sys.path.append('src/tic_tac_toe/fogel')
from game import *
from fogel_neural_net import *
from random_player import *
from neural_net_player import *


net = NeuralNet.create_net()
print(net.get_net_output([1,-1,0,0,1,-1,0,0,0]))
# net.forward_propagate([1,-1,0,0,1,-1,0,0,0])

# players = [NeuralNetPlayer(), RandomPlayer()]

# game = Game(players)
# game.run()
# print(game.winner)



