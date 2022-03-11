import random

class DictPlayer():
  def __init__(self, index):
    self.index = index
    self.score = 0
    self.player_number = None
    self.board = None
    self.strategy = {}
    self.create_strategy()

  def set_player_number(self, n):
    self.player_number = n

  def create_strategy(self):
    temp_board = []

    for i in range(3**9): 
      c = i
      temp_board = []
      for _ in range(9): 
        temp_board.append(c % 3)
        c = c // 3
      if abs(temp_board.count(1)-temp_board.count(2)) <= 1 and 0 in temp_board:
        temp_board = ''.join(map(str, temp_board))
        open_spaces = self.find_open_indices(temp_board)
        move = random.choices(open_spaces)[0]
        self.strategy[temp_board] = move
  
  def find_open_indices(self, board_string):
    open_indices = []
    for index, value in enumerate(board_string):
      if value == '0':
        open_indices.append(index)
    return open_indices
    
  def choose_space(self, possible_moves, board):
    string_board = self.board_to_string(board)
    chosen_move = self.index_to_coords(self.strategy[string_board])
    return chosen_move

  def board_to_string(self, board):
    board = self.nones_to_zeros(board)
    return ''.join([''.join(row) for row in board])

  def string_to_board(self, string):
    board = [[int(string[i+3*j]) if int(string[i+3*j]) != 0 else None  for i in range(3)] for j in range(3)]
    return board

  def nones_to_zeros(self, board):
    return [map(str,(map(lambda x: 0 if x is None else x, row))) for row in board]

  def index_to_coords(self, index):
    return (int((index-index%3)/3), int(index%3))

  def coords_to_index(self, coords):
    return 3*coords[0]+coords[1]
  