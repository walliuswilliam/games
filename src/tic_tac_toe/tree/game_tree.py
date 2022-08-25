class Node():
    def __init__(self, state, player):
        self.state = state
        self.turn = 1 if self.state.count('1') == self.state.count('2') else 2
        self.player = player
        self.winner = self.check_winner()
        self.children = []
        self.parent = None
        self.score = None
    

    def set_score(self):
        if len(self.children) == 0:
            if self.winner == self.player:
                self.score = 1
            elif self.winner == 3 - self.player:
                self.score = -1
            elif self.winner == 'Tie':
                self.score = 0
            return

        #print([child.state for child in self.children])
        if self.turn == self.player:
            self.score = max(self.get_children_scores())
        elif self.turn == 3 - self.player:
            self.score = min(self.get_children_scores())

    def get_children_scores(self):
        if len(self.children) == 0:
            return
        for child in self.children:
            child.set_score()
        return [child.score for child in self.children]

    def check_winner(self):
        state = self.state
        rows = [[state[i+3*j] for i in range(3)] for j in range(3)]
        cols = [[state[j+3*i] for i in range(3)] for j in range(3)]
        diags = [[state[i+3*i] for i in range(3)],[state[i+3*(2-i)] for i in range(3)]]

        for i in (rows + cols + diags):
            if len(set(i)) == 1 and '0' not in i:
                return int(i[0])

        if not any('0' in row for row in state):
            return 'Tie'


class GameTree():
    def __init__(self, player):
        self.root = Node('000000000', player)
        self.player = player
        self.nodes = [self.root]
        self.leaf_nodes = []
        self.states = {self.root.state:self.root}


    def construct_tree(self):
        queue = [self.root]
        while len(queue) != 0:
            current_node = queue[0]
            if current_node.winner is None:
                moves = self.find_open_spaces(current_node.state)
                for move in moves:
                    state = current_node.state
                    new_state = self.update_board(state, move, current_node.turn)
                    if new_state in self.states:
                        new_node = self.states[new_state]
                    else:
                        new_node = Node(new_state, self.player)
                        self.nodes.append(new_node)
                        self.states[new_state] = new_node
                        queue.append(new_node)
                        
                    current_node.children.append(new_node)
                    new_node.parent = current_node
            else:
                self.leaf_nodes.append(current_node)
            queue.remove(current_node)

    def set_node_scores(self):
        assert len(self.root.children) != 0, "create game tree before setting scores"
        self.root.set_score()
    
    def find_open_spaces(self, board):
        return [i for i in range(len(board)) if board[i] == '0']

    def update_board(self, board, index, value):
        board = [i for i in board]
        board[index] = str(value)
        return ''.join(board)

    def print_states(self, state):
        print("\n-------")
        board = [[self.board[i+3*j] for i in range(3)] for j in range(3)]
        for row in board:
            for element in row[:-1]:
                print(element, end="  ")
            print(row[-1])
        print("-------")
