import sys

sys.path.append('src/checkers')
from checkers import Checkers
sys.path.append('src/checkers/players')
from random_player import *
from input_player import *


# players = [RandomPlayer(), RandomPlayer()]
players = [InputPlayer(), RandomPlayer()]

game = Checkers(players)

game.run(debug=True, symbols=True)
print(f'Winner: Player {game.winner}')
