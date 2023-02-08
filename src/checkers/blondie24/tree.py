import sys
sys.path.append('./src/checkers/')
from checkers.checkers import Checkers

class Node():
    def __init__(self, state, player_num):
        self.state = state
        self.turn = self.set_turn()
        self.player_num = player_num
        self.winner = self.check_winner()
        self.children = []
        self.parent = None
        self.score = None
    

    def set_turn(self):
        p1_count = 0
        p2_count = 0
        for row in self.state:
            p1_count += row.count('1')
            p2_count += row.count('2')
        if p1_count == p2_count:
            return 1
        else:
            return 2

    def get_children_scores(self):
        if len(self.children) == 0:
            return
        for child in self.children:
            child.set_score()
        return [child.score for child in self.children]

    def check_winner(self):
        state = self.string_to_list(self.state)
        if not any('0' in row for row in state):
            self.winner = 'tie'
        
        rows = self.four_in_list(state)
        if rows:
            self.winner = rows

        cols = self.four_in_list([''.join(i) for i in zip(*state)])
        if cols:
            self.winner = cols

        diag = self.four_in_list(self.get_diags(state))
        if diag:
            self.winner = diag
    


class Tree():
    def __init__(self, player_num):
        self.root = Node([[(i + j) % 2 * ((3 - ((j < 3) - (j > 4))) % 3) for i in range(8)] for j in range(8)], player_num)
        self.player_num = player_num
        self.nodes = [self.root]
        self.leaf_nodes = []
        self.states = {self.root.state:self.root}


    def construct_tree(self, starting_node_state, n):
        try:
            starting_node = self.states[starting_node_state]
        except:
            starting_node = Node(starting_node_state, self.player_num)
            self.nodes.append(starting_node)
            self.states[starting_node_state] = starting_node
        
        
        
        
        
        
        
        try:
            starting_node = self.states[starting_node_state]
        except:
            starting_node = Node(starting_node_state, self.player_num)
            self.nodes.append(starting_node)
            self.states[starting_node_state] = starting_node
        
        self.root = starting_node

        ending_depth = self.calc_game_depth(starting_node.state) + n
        queue = [starting_node]
        while len(queue) != 0:
            current_node = queue[0]
            if self.calc_game_depth(current_node.state) >= ending_depth:
                queue.remove(current_node)
                continue
            if current_node.winner is None:
                moves = self.find_open_spaces(self.string_to_list(current_node.state))
                for move in moves:
                    state = current_node.state
                    new_state = self.update_board(state, move, current_node.turn)
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

    def calc_game_depth(self, state):
        total = 0
        for row in state:
            total += row.count('0')
        return 42-total

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

    def update_board(self, board, index, value):
        board = self.string_to_list(board)
        cols = [''.join(i) for i in zip(*board)]
        chosen_col = [*cols[index]]

        col_idx = len(chosen_col)-1 - list(reversed(chosen_col)).index('0')
        row = board[col_idx]
        board[col_idx] = row[:index] + str(value) + row[index+1:]
        return self.list_to_string(board)
    
    def state_to_string(state):
        state_str = ''
        for sublist in state:
            for item in sublist:
                state_str += str(item)
        return state_str

    def string_to_state(state_str):
        state = []
        sublist = []
        for i, c in enumerate(state_str):
            sublist.append(int(c))
            if (i + 1) % 8 == 0:
                state.append(sublist)
                sublist = []
        return state
