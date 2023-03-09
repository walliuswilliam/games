import random

class Checkers:
    def __init__(self, players):
        self.players = players
        self.board = [[(i + j) % 2 * ((3 - ((j < 3) - (j > 4))) % 3) for i in range(8)] for j in range(8)]
        self.turn = 1
        self.winner = None
        self.set_player_nums()


    def set_player_nums(self):
        for i, player in enumerate(self.players):
            player.player_num = i+1

    def get_moves(self, player_num, board=None):
        if board == None: board = self.board

        possible_moves = []

        # loop through all coordinates
        

        for i in range(8):
            for j in range(8):

                current_coords = [i, j]
                current_piece = board[i][j]

                # check if there is a piece on the current coord

                if abs(current_piece) == player_num:

                    # get moves that the piece might be able to do

                    moves_to_check = self.add_moves_to_check(current_piece, current_coords, [], [])

                    while len(moves_to_check) > 0:

                        # check first move in moves_to_check

                        move_to_check = moves_to_check.pop(0) # moves_to_check is a queue
                        coord, translation_to_check, captured_coords = move_to_check

                        new_i, new_j = self.apply_translation((coord, translation_to_check))
                        if new_i < 0 or new_i > 7 or new_j < 0 or new_j > 7: continue
                        new_piece = board[new_i][new_j]
                        
                        # check if the new spot is empty

                        if abs(new_piece) == 0 and captured_coords == []:
                            possible_moves.append(move_to_check)
                    
                        # check if the opponent is in the new spot

                        elif abs(new_piece) == 3 - player_num:
                            
                            # if so, and if the next next spot is empty, add that spot to moves_to_check

                            next_translation = [2*t for t in translation_to_check]
                            new_new_i, new_new_j = self.apply_translation((coord, next_translation))
                            if new_new_i < 0 or new_new_i > 7 or new_new_j < 0 or new_new_j > 7: continue
                            new_new_piece = board[new_new_i][new_new_j]

                            if abs(new_new_piece) == 0 and not self.nested_list_in_list(captured_coords, [new_i, new_j]):

                                # add capture to possible moves

                                previous_translation = self.get_translation(coord, current_coords)
                                new_translation = self.apply_translation((previous_translation, next_translation))
                                new_captured_coords = captured_coords + [[new_i, new_j]]
                                possible_moves.append([current_coords, new_translation, new_captured_coords])

                                # add potential to combo captures

                                next_next_coords = self.apply_translation((current_coords, new_translation))
                                moves_to_check = self.add_moves_to_check(current_piece, next_next_coords, new_captured_coords, moves_to_check)

                                # then, it'll loop back to the start of moves_to_check
        
        return possible_moves

    def add_moves_to_check(self, current_piece, current_coords, captured_coords, moves_to_check):
        
        direction = 1 - 2*(current_piece % 2)

        moves_to_check.append([current_coords, [direction, -1], captured_coords])
        moves_to_check.append([current_coords, [direction, 1], captured_coords])

        if current_piece < 0:
            moves_to_check.append([current_coords, [-direction, -1], captured_coords])
            moves_to_check.append([current_coords, [-direction, 1], captured_coords])
        
        return moves_to_check

    def lists_are_equal(self, list1, list2):
        if len(list1) != len(list2): return False
        for i in range(len(list1)):
            if list1[i] != list2[i]: return False
        return True

    def nested_list_in_list(self, parent_list, nested_list):
        for l in parent_list:
            if all(x == y for x, y in zip(l, nested_list)):
                return True
        return False
    
    def check_crowns(self, input_board=None):
        if input_board: board = input_board
        else: board = self.board
        for idx in range(len(board[0])):
            if board[0][idx] == 1:
                board[0][idx] = -1
        for idx in range(len(board[-1])):
            if board[-1][idx] == 2:
                board[-1][idx] = -2
        if input_board: return board

    def apply_translation(self, move):
        return [move[0][0] + move[1][0], move[0][1] + move[1][1]]
    
    def get_translation(self, coord1, coord2):
        return [coord1[0] - coord2[0], coord1[1] - coord2[1]]

    def remove_piece(self, coords, input_board=None):
        if input_board: board = input_board
        else: board = self.board
        board[coords[0]][coords[1]] = 0
        if input_board: return board

    def check_winner(self, board=None):
        if not board: board = self.board
        if {i for row in board for i in row} == {0}:
            return 'tie'
        elif not any(1 in row for row in board) and not any(-1 in row for row in board):
            return 2
        
        elif not any(2 in row for row in board) and not any(-2 in row for row in board):
            return 1

    def run_turn(self, player, debug=False, symbols=False):
        if debug: self.print_board(symbols=symbols)
        possible_moves = self.get_moves(player.player_num)
            
        if len(possible_moves) == 0:
            self.winner = 3-player.player_num
            return
        move = player.choose_move([row.copy() for row in self.board], possible_moves)
        if move not in possible_moves:
            print('Invalid Move')
            move = random.choice(possible_moves)
        if move[1] == (0,0):
            return

        if debug: print('Move:', move)
        new_move = self.apply_translation(move)
        self.board[new_move[0]][new_move[1]] = self.board[move[0][0]][move[0][1]]
        for coord in move[2]:
            self.remove_piece(coord)
        self.remove_piece(move[0])
        self.check_crowns()

    def run(self, num_turns=250, debug=False, symbols=False):
        for i in range(1, 2*num_turns):
            if i % 2 == 0:
                self.turn += 1
            if debug:
                print(f'\nPlayer {self.players[((i+1) % 2)].player_num} turn') 
            self.run_turn(self.players[(i % 2) - 1], debug=debug, symbols=symbols)
            if not self.winner:
                self.winner = self.check_winner()
            if self.winner:
                return self.winner
        if debug: print('Game Over: Max Turns Reached')
    
    def print_board(self, board=None, symbols=False):
        if not board:
            board = self.board
        if symbols:
            print('   ', *range(8), '\n    ―――――――――――――――')
            for i, row in enumerate(board):
                symbols = {-1:'♚', 1:'⬤', -2:'♔', 2:'◯', 0:'⬚'}
                row = [symbols[i] for i in row]
                print(i, '|', *row, sep=' ')

        else:
            print('   ', *range(8), '\n    ―――――――――――――――')
            for i, row in enumerate(board):
                print(i, '|', *row, sep=' ')
