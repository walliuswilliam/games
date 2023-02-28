import sys
sys.path.append('./src/checkers/blondie24')
from neural_net import *
from tree import *


class NeuralNetPlayer:
    def __init__(self):
        self.player_num = None
        self.net = None
        self.tree = None


    def choose_move(self, board, possible_moves):
        if not self.net: self.net = NeuralNet.create_net(self.player_num)
        if not self.tree: self.tree = Tree(self.player_num)

        self.tree.construct_tree(board)

        board_node = self.tree.states[Tree.state_to_string(self, board)]
        self.set_node_score(board_node)

        max_child = board_node.children[0]
        for child in board_node.children:
            if child.score > max_child.score:
                max_child = child
        
        print(max_child)
        quit()
        
        


        
        pass

        # board = self.convert_board(board)

        # assert sum(board) == 0, 'Board sum is not 0'
        # for i in set(board): assert i in [-1,0,1], 'Invalid board state'
        
        # net_output = self.net.get_net_output(board)
        # net_output_tup = [(i,val) for i, val in enumerate(net_output)]
        # available_moves = [i for i in net_output_tup if i[0] in possible_moves]
        # return max(available_moves, key=lambda item:item[1])[0]

    def set_node_score(self, node):
        if len(node.children) == 0:
            if node.winner == self.player_num:
                node.score = 1
            elif node.winner == 3 - self.player_num:
                node.score = -1
            else:
                node.score = self.net.get_net_output(Tree.string_to_state(self, node.state))
            return
        
        node.score = max(self.get_children_scores(node))
        

    def get_children_scores(self, root_node):
        if len(root_node.children) == 0:
            return
        for child in root_node.children:
            self.set_node_score(child)
        return [child.score for child in root_node.children]


    def update_board(self, index, value, board):
        board = [i for i in board]
        board[index] = str(value)
        return ''.join(board)
