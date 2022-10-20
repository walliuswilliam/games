import random

class RandomPlayer:
    def __init__(self):
        self.player_num = None
        self.invalid_moves = 0
  

    def set_player_num(self, n):
        self.player_num = n

    def choose_move(self, board, possible_moves):
        return random.choice(possible_moves)
