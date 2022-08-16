import copy

class Node():
  def __init__(self, state, player):
    self.state = state
    self.player = player
    self.winner = None
    self.children = None
  
  def check_for_winner(self):
    rows = self.state.copy()
    cols = [[self.state[i][j] for i in range(3)] for j in range(3)]
    diags = [[self.state[i][i] for i in range(3)],
             [self.state[i][2-i] for i in range(3)]]

    board_full = True
    for row in rows + cols + diags:
      if None in row:
        board_full = False

      for player in [1,2]:
        if row == [player for _ in range(3)]:
          return player
    
    if board_full:
      return 'Tie'
    return None



  
#   def find_open_indices(self, board_string):
#     open_indices = []
#     for index, value in enumerate(board_string):
#       if value == '0':
#         open_indices.append(index)
#     return open_indices
    
#   def choose_space(self, possible_moves, board):
#     string_board = self.board_to_string(board)
#     chosen_move = self.index_to_coords(self.strategy[string_board])
#     return chosen_move

#   def board_to_string(self, board):
#     board = [[str(i) for i in row] for row in board]
#     if self.player_number == 2:
#       board = self.swap_nums(board)

#     return ''.join([''.join(row) for row in board])

#   def string_to_board(self, string):
#     board = [[],[],[]]
#     for row_index, row in enumerate(board):
#       for i in range(3):
#         row.append(int(string[(row_index*3)+i]))

#     if self.player_number == 2:
#       board = [[int(i) for i in row] for row in self.swap_nums(board)]
#     return board

#   def swap_nums(self, board):
#     board = [[3-int(i) if int(i) != 0 else int(i) for i in row ] for row in board]
#     return [[str(i) for i in row] for row in board]

#   def index_to_coords(self, index):
#     return (int((index-index%3)/3), int(index%3))

#   def coords_to_index(self, coords):
#     return 3*coords[0]+coords[1]
  


class GameTree():
    def __init__(self, starting_player):
        self.root = Node([[None for _ in range(3)] for _ in range(3)], starting_player)
        # self.states = self.create_state_dict()
        # print(len(self.states))
        # for state in self.states.keys():
        #     print(self.print_states(state))
        self.leaf_nodes = 0


    def string_to_board(self, string):
        board = [[],[],[]]
        for row_index, row in enumerate(board):
            for i in range(3):
                row.append(int(string[(row_index*3)+i]))
        return board


    def print_states(self, state):
        state = self.string_to_board(state)
        print("\n-------")
        for row in state:
            for element in row[:-1]:
                print(element, end="  ")
            print(row[-1])
        print("-------")

    def create_state_dict(self):
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
                strategy[temp_board] = Node(temp_board)
        return strategy


    def contruct_tree(self):
        self.set_children(self.root)
        current_layer = self.root.children
        while len(current_layer) != 0:
            next_layer = self.get_next_layer(current_layer)
            current_layer = next_layer

    def get_next_layer(self, layer):
        new_layer = []
        for child in layer:
            winner = child.check_for_winner()
        if winner is None:
            self.set_children(child)
            for sub_child in child.children:
                new_layer.append(sub_child)
        else:
            child.winner = winner
            self.leaf_nodes += 1

        return new_layer

    def set_children(self, parent):
        children = []
        for row_index in range(len(parent.state)):
            for column_index in range(len(parent.state[row_index])):
                if parent.state[row_index][column_index] is None:
                    child = copy.deepcopy(parent.state)
                    child[row_index][column_index] = self.opposite_player(parent.player)
                    children.append(Node(child, self.opposite_player(parent.player)))
        parent.children = children


    def opposite_player(self, player):
        if player == None:
            return None
        elif player == 1:
            return 2
        elif player == 2:
            return 1