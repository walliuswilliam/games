import sys
sys.path.append('src/tic_tac_toe')
from game import *
from game_tree import *
from random_player import *


game = GameTree(1)

game.contruct_tree()
print(game.leaf_nodes, 'leaf nodes')