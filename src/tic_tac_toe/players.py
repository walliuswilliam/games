import random, sys
sys.path.append('src/tic_tac_toe/tree')
from game_tree import *

class RandomPlayer:
  def __init__(self):
    self.player_num = None

  def set_player_num(self, n):
    self.player_num = n
  
  def choose_space(self, possible_moves, board):
    return possible_moves[random.randrange(len(possible_moves))]

class MinimaxPlayer:
  def __init__(self):
    self.player_num = None
    

  def set_player_num(self, n):
    self.player_num = n
    self.tree = GameTree(self.player_num)
    self.tree.construct_tree()
    self.tree.set_node_scores()
  
  def set_minimax_values(self):
    leaf = self.tree.leaf_nodes.copy()
    for node in leaf:
      if node.winner == self.player_num:
        node.minimax_val = 1
      elif node.winner == 3-self.player_num:
        node.minimax_val = -1
      else:
        node.minimax_val = 0
    print('leaf', len(leaf))
    queue = [child for child in node.parent.children for node in leaf]
    print('queue', len(queue), [n.minimax_val for n in queue])
    visited = []
    while len(queue) != 0:
      
      print(len(queue))
      print(queue[0].children)
      node = queue[0]

      skip = False
      print('g', [n.minimax_val for n in node.parent.children])
      for child in node.parent.children:
        if child not in visited and child not in queue and child.minimax_val == None:
          skip = True
          queue.insert(0, child)
      print(len(queue))
      if skip:
        continue
        
      
      if None in [i.minimax_val for i in node.parent.children]:
        print([n.minimax_val for n in node.parent.children])

      node_children_vals = [c.minimax_val for c in node.parent.children]
      print(node_children_vals)
      if node.player == self.player_num:
        node.minimax_val = max(node_children_vals)
      elif node.player == 3-self.player_num:
        node.minimax_val = min(node_children_vals)
      visited.append(node)
      queue.pop(node)
      # curr_node = node.parent
      # while curr_node != self.tree.root:
      #   children = curr_node.children
      #   #for child in children:

      #   if curr_node.player == self.player_num:
      #     curr_node.minimax_val = node.minimax_val
      #   elif curr_node.player == 3-self.player_num:
      #     curr_node.minimax_val = node.minimax_val
      #   else:
      #     curr_node.minimax_val = node.minimax_val
      #   curr_node = curr_node.parent
      
      # # print(curr_node.state)
      # # quit()
      
  def update_board(self, index, value, board):
    board = [i for i in board]
    board[index] = str(value)
    return ''.join(board)

  def choose_space(self, possible_moves, board):
    # if board.count('0') > 7:
    #   self.set_minimax_values()

    # print(board)
    moves = []
    best_move, best_move_idx = self.update_board(possible_moves[0], self.player_num, board), possible_moves[0]

    # print(possible_moves)
    for move in possible_moves:
      temp_board = self.update_board(move, self.player_num, board)
      # print(temp_board, self.tree.states[temp_board].score)
      if self.tree.states[temp_board].score > self.tree.states[best_move].score:
        best_move, best_move_idx = temp_board, move
      # print('best', best_move, self.tree.states[best_move].minimax_val,'\n')

    return best_move_idx

    