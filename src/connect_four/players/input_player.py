class InputPlayer:
    def __init__(self):
        self.player_num = None
        self.invalid_moves = 0
  

    def set_player_number(self, n):
        self.player_num = n

    def choose_move(self, board, possible_moves):
        for row in board:
            print(" ".join(row))
        while True:
            move = input(f"Player {self.player_num}'s turn: ")
            if move == 'moves':
                print(possible_moves)
            elif int(move) in possible_moves:
                break
            else:
                print('Invalid move')
        return int(move)
        