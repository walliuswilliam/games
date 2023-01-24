import random

class RandomPlayer:
    def __init__(self):
        self.player_num = None

    def choose_move(self, board, possible_moves):
        return random.choice(possible_moves)