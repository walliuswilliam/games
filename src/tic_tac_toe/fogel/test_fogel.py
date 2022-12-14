import sys
sys.path.append('src/tic_tac_toe')
sys.path.append('src/tic_tac_toe/players')
sys.path.append('src/tic_tac_toe/fogel')
from game import *
from fogel_neural_net import *
from random_player import *
from neural_net_player import *


# net = NeuralNet.create_net()
# print(net.get_net_output([1,-1,0,0,1,-1,0,0,0]))

# players = [NeuralNetPlayer(), RandomPlayer()]

# game = Game(players)
# game.run()
# print(game.winner)


gen = create_initial_generation()
gen_2 = create_new_generation(gen)

print(best_net_score(gen))
print(best_net_score(gen_2))

# num_games = 20
# num_wins = {1: 0, 2: 0, 'ties': 0}
# players = [NeuralNetPlayer(), RandomPlayer()]

# for i in range(num_games//2):
#     # print(i)
#     game = Game(players)
#     game.run()
#     if game.winner != 'Tie':
#         num_wins[game.winner] += 1
#     else:
#         num_wins['ties'] += 1
# players.reverse()
# for i in range(num_games//2):
#     # print(i+num_games//2)
#     game = Game(players)
#     game.run()
#     if game.winner != 'Tie':
#         num_wins[3-game.winner] += 1
#     else:
#         num_wins['ties'] += 1

# print(num_wins)