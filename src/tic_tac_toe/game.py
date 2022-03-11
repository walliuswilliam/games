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
    spaces = [(i,j) for i in range(3) for j in range(3) if board[i][j] == None]
    return spaces

  def complete_turn(self, player_number):
    player = self.players[player_number-1]
    open_spaces = self.find_open_spaces(self.board)
    chosen_move = player.choose_space(open_spaces, self.board)
    if chosen_move not in open_spaces:
      raise Exception('Invalid Move Chosen')
    self.board[chosen_move[0]][chosen_move[1]] = player_number
  
  def check_winner(self):
    board = self.board.copy()
    rows = board
    cols = [[board[i][j] for i in range(3)] for j in range(3)]
    diags = [[board[i][i] for i in range(3)],[board[i][2-i] for i in range(3)]]
    
    for i in (rows + cols + diags):
      if len(set(i)) == 1 and None not in i:
        self.winner = i[0]

    if self.winner == None:
      if not any(None in row for row in self.board):
        self.winner = 'Tie'

  def run_to_completion(self):
    while self.winner is None:
      self.complete_turn(self.starting_player)
      self.check_winner()
      if self.winner is not None:
        return self.winner

      self.complete_turn(3-self.starting_player)
      self.check_winner()
      if self.winner is not None:
        return self.winner
    return self.winner
