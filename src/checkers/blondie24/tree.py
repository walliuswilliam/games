import sys
sys.path.append('.\src\checkers')
from checkers import Checkers

class Node:
    def __init__(self, state, player_num):
        self.state = state
        self.player_num = player_num
        self.winner = Checkers.check_winner(self, Tree.string_to_state(self, self.state))
        self.children = []
        self.parent = None
        self.score = None


class Tree:
    def __init__(self, player_num):
        root_state = self.state_to_string([[(i + j) % 2 * ((3 - ((j < 3) - (j > 4))) % 3) for i in range(8)] for j in range(8)])
        self.root = Node(root_state, player_num)
        self.player_num = player_num
        self.nodes = [self.root]
        self.leaf_nodes = []
        self.states = {self.root.state:self.root}


    def construct_tree(self, starting_node_state, d=2):
        starting_state = self.state_to_string(starting_node_state)
        try:
            starting_node = self.states[starting_state]
        except:
            starting_node = Node(starting_state, self.player_num)
            self.nodes.append(starting_node)
            self.states[starting_state] = starting_node

        self.root = starting_node

        queue = [starting_node]
        while len(queue) != 0:
            current_node = queue[0]
            
            if not self.check_if_node_within_depth(current_node, d) and current_node != self.root:
                queue.remove(current_node)
                continue

            if current_node.winner is None:
                moves = Checkers.get_moves(self, self.player_num, self.string_to_state(current_node.state))
                for move in moves:
                    state = current_node.state
                    new_state = self.state_to_string(self.update_board(self.string_to_state(state), move))
                    if new_state in self.states:
                        new_node = self.states[new_state]
                    else:
                        new_node = Node(new_state, self.player_num)
                        self.nodes.append(new_node)
                        self.states[new_state] = new_node
                        queue.append(new_node)
                        
                    current_node.children.append(new_node)
                    new_node.parent = current_node
            else:
                self.leaf_nodes.append(current_node)
            queue.remove(current_node)

    def update_board(self, board, move):
        new_coords = Checkers.apply_translation(self, move)

        board[new_coords[0]][new_coords[1]] = board[move[0][0]][move[0][1]]
        for coord in move[2]:
            board = Checkers.remove_piece(self, coord, input_board=board)
        board = Checkers.remove_piece(self, move[0], input_board=board)
        board = Checkers.check_crowns(self, input_board=board)
        return board

    def check_if_node_within_depth(self, node, d):
        cur_node = node
        if cur_node == self.root: return True
        for i in range(d):
            if cur_node.parent == self.root:
                return True
            else:
                cur_node = cur_node.parent
        
        return False

    def set_node_scores(self):
        assert len(self.root.children) != 0, "create game tree before setting scores"
        self.root.set_score()
    
    def find_open_spaces(self, board):
        moves = Checkers.find_moves(self.player)
        moves = []
        t_board = [''.join(i) for i in zip(*board)]
        for i, col in enumerate(t_board):
            if '0' in col:
                moves.append(i)
        return moves
    
    def state_to_string(self, state):
        state_str = ''
        for sublist in state:
            for item in sublist:
                if item == -1:
                    state_str += str(3)
                elif item == -2:
                    state_str += str(4)
                else:
                    state_str += str(item)
        return state_str

    def string_to_state(self, state_str):
        state = []
        sublist = []
        for i, c in enumerate(state_str):
            try:
                if c == '3':
                    sublist.append(int(-1))
                elif c == '4':
                    sublist.append(int(-2))
                else:
                    sublist.append(int(c))
            except:
                print('state str', state_str)
                print('c', c)
                raise Exception()
            if (i + 1) % 8 == 0:
                state.append(sublist)
                sublist = []
        return state

    def add_moves_to_check(self, current_piece, current_coords, captured_coords, moves_to_check): return Checkers.add_moves_to_check(self, current_piece, current_coords, captured_coords, moves_to_check)
    def apply_translation(self, move): return Checkers.apply_translation(self, move)
    def get_translation(self, coord1, coord2): return Checkers.get_translation(self, coord1, coord2)
    # def lists_are_equal(self, list1, list2): return Checkers.lists_are_equal(self, list1, list2)
    def nested_list_in_list(self, parent_list, nested_list): return Checkers.nested_list_in_list(self, parent_list, nested_list)


    
    # def get_translation(self, coord1, coord2):