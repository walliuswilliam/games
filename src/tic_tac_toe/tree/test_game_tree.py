import sys
sys.path.append('src/tic_tac_toe')
from game import *
from game_tree_canonical import *
from game_tree import *
from random_player import *


# game = GameTreeCanon()

# game.construct_tree()
# print(len(game.leaf_nodes)) #255168


game = GameTree()

game.construct_tree()
print(len(game.nodes)) #5478