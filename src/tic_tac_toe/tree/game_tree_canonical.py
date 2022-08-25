class Node():
    def __init__(self, state):
        self.state = state
        self.player = 1 if self.state.count('1') == self.state.count('2') else 2
        self.winner = self.check_winner()
        self.children = []
  

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

class GameTreeCanon():
    def __init__(self, starting_player=1):
        self.root = Node('000000000')
        self.nodes = [self.root]
        self.leaf_nodes = []


    def contruct_tree(self):
        queue = [self.root]
        while len(queue) != 0:
            current_node = queue[0]
            if current_node.winner is None:
                moves = self.find_open_spaces(current_node.state)
                for move in moves:
                    state = current_node.state
                    new_node = Node(self.update_board(state, move, current_node.player))
                    current_node.children.append(new_node)
                    new_node.parent = current_node
                    self.nodes.append(new_node)
                    queue.append(new_node)
            else:
                self.leaf_nodes.append(current_node)
            queue.remove(current_node)
    
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
