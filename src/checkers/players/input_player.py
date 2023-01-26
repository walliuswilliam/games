class InputPlayer:
    def __init__(self):
        self.player_num = None

    def choose_move(self, board, possible_moves):
        choice = int(input(f'Moves: {[f"{i}: {move}" for i, move in enumerate(possible_moves)]}\nChoose Move: '))
        while choice not in range(len(possible_moves)):
            print('Invalid Choice')
            choice = int(input(f'Moves: {[f"{i}: {move}" for i, move in enumerate(possible_moves)]}\nChoose Move: '))
        
        return possible_moves[choice]