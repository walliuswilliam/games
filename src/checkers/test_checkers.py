import sys

sys.path.append('src/checkers')
from checkers import Checkers
sys.path.append('src/checkers/players')
from random_player import *
from input_player import *


players = [RandomPlayer(), RandomPlayer()]

game = Checkers(players)
game.run(debug=True)
print(f'Winner: Player {game.winner}')
# game.print_board()
# game.run_turn(game.players[0])
# game.print_board()


# print(game.check_winner())

# game.board = [[0,0,0,0,1,2,0,0],[],[],[],[],[],[],[0,0,0,0,1,2,0,0]]
# game.check_crowns()
# n_board = [row.copy() for row in game.board]
# n_board[0][0] = 100
# print(n_board)
# print(game.board)
# print(game.board)
# game.run()
# print(game.winner)
