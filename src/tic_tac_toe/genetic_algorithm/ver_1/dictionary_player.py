import random
random.seed(1)

class DictPlayer():
  def __init__(self, strategy=None):
    self.index = None
    self.score = 0
    self.player_number = None
    self.board = None
    self.strategy = strategy
    if self.strategy == None:
      self.create_strategy()

  def set_player_number(self, n):
    self.player_number = n

  def create_strategy(self):
    strategy = {}
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
        strategy[temp_board] = move
        self.strategy = strategy
    with open('strat.txt', 'w') as f:
      f.write('dict = ' + str(strategy) + '\n')  
  
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
    board = [[str(i) for i in row] for row in board]
    if self.player_number == 2:
      board = self.swap_nums(board)

    return ''.join([''.join(row) for row in board])

  def string_to_board(self, string):
    board = [[],[],[]]
    for row_index, row in enumerate(board):
      for i in range(3):
        row.append(int(string[(row_index*3)+i]))

    if self.player_number == 2:
      board = [[int(i) for i in row] for row in self.swap_nums(board)]

    return board

  def swap_nums(self, board):
    new_board = [[],[],[]]
    for row_index, row in enumerate(board):
      for i in row:
        if i == 1:
          new_board[row_index].append('2')
        elif i == 2:
          new_board[row_index].append('1')
        else:
          new_board[row_index].append(str(i))
    return new_board

  def index_to_coords(self, index):
    return (int((index-index%3)/3), int(index%3))

  def coords_to_index(self, coords):
    return 3*coords[0]+coords[1]
  