import random

class RandomPlayer:
    def __init__(self):
        self.player_num = None

    def set_player_num(self, n):
        self.player_num = n

    def choose_space(self, possible_moves, board):
        return possible_moves[random.randrange(len(possible_moves))]