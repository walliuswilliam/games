import random

class RandomPlayer:
    def __init__(self):
        self.number = None
        self.invalid_moves = 0
  

    def set_player_number(self, n):
        self.number = n

    def choose_move(self, board, possible_moves):
        return random.choice(possible_moves)
