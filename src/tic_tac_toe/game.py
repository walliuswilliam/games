import sys
sys.path.append('src/tic_tac_toe')
from player import *
import numpy as np

class Game():
  def __init__(self, players, starting_player=1):
    self.players = players
    self.set_player_numbers()
    self.starting_player = starting_player

    self.board = [[None,None,None],
                  [None,None,None],
                  [None,None,None]]
    self.winner = None
    
  
  def set_player_numbers(self):
    for i, player in enumerate(self.players):
      player.set_player_number(i+1)
  
  def find_open_spaces(self, board):
    spaces = []
    for row_index in range(len(board)):
      for column_index in range(len(board[row_index])):
        if board[row_index][column_index] == None:
          spaces.append((row_index, column_index))
    return spaces

  def complete_turn(self, player_number):
    chosen_move = self.players[player_number-1].choose_space(self.find_open_spaces(self.board))
    self.board[chosen_move[0]][chosen_move[1]] = player_number
  
  def check_winner(self):
    for row_index in range(len(self.board)):
      if len(set(self.board[row_index])) <= 1:
        if self.board[row_index][0] != None:
          self.winner = self.board[row_index][0]
    
    transpose_board = np.array(self.board).transpose()
    for col_index in range(len(transpose_board)):
      if len(set(transpose_board[col_index])) <= 1:
        if transpose_board[col_index][0] != None:
          self.winner = transpose_board[col_index][0]
    
    diagonal_index_1 = [0,1,2]
    diagonal_index_2 = [2,1,0]
    diagonals = []

    for num in range(2):
      temp_list = []
      if num == 0:
        for row in self.board:
          temp_list.append(row[diagonal_index_1[self.board.index(row)]])
        diagonals.append(temp_list)
      if num == 1:
        for row in self.board:
          temp_list.append(row[diagonal_index_2[self.board.index(row)]])
        diagonals.append(temp_list)
    
    for diagonal in diagonals:
      if len(set(diagonal)) <= 1:
        if diagonal[0] != None:
          self.winner = diagonal[0]

    if self.winner == None:
      if not any(None in row for row in self.board):
        self.winner = 'Tie'

  def opposite_player(self, player_number):
    if player_number == None:
      return None
    elif player_number == 1:
      return 2
    elif player_number == 2:
      return 1

  def run_to_completion(self):
    while self.winner is None:
      self.complete_turn(self.starting_player)
      self.check_winner()
      if self.winner is not None:
        return self.winner

      self.complete_turn(self.opposite_player(self.starting_player))
      self.check_winner()
      if self.winner is not None:
        return self.winner
    return self.winner
      


  




  
