class InputPlayer:
    def __init__(self):
        self.player_num = None

    def choose_move(self, board, possible_moves):
        choice = input(f'Moves: {[f"{i}: {move}" for i, move in enumerate(possible_moves)]}\nChoose Move: ')
        try: 
            choice = int(choice)
        except: pass
        while choice not in range(len(possible_moves)):
            print('Invalid Choice\n')
            choice = input(f'Moves: {[f"{i}: {move}" for i, move in enumerate(possible_moves)]}\nChoose Move: ')
            try: 
                choice = int(choice)
            except: pass
        
        return possible_moves[choice]