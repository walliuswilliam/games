import random

class RandomPlayer():
  def __init__(self):
    self.player_number = None
    self.board = None

  def set_player_number(self, n):
    self.player_number = n
  
  def choose_space(self, possible_moves, board):
    return possible_moves[random.randrange(len(possible_moves))]
