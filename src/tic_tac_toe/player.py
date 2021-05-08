import random

class Player():
  def __init__(self):
    self.player_number = None

  def set_player_number(self, n):
    self.player_number = n
  
  def choose_space(self, possible_moves):
    return possible_moves[random.randrange(len(possible_moves))]
  
