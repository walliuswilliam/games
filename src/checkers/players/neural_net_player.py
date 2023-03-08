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
        print(f'possible moves: {possible_moves}')
        if not self.net: self.net = NeuralNet.create_net(self.player_num)
        if not self.tree: self.tree = Tree(self.player_num)

        self.tree.construct_tree(board)

        board_node = self.tree.states[Tree.state_to_string(self, board)]
        self.set_node_score(board_node)

        max_child = board_node.children[0]
        for child in board_node.children:
            if child.score > max_child.score:
                max_child = child
        
        print([i.score for i in board_node.children])
        print(max_child.score)
        # print(Checkers.print_board(self, board=Tree.string_to_state(self, max_child.state)))
        for move in possible_moves:
            print(move)
            print('baord', board)
            temp_board = self.update_board(board, move)
            print('tb', temp_board)
            quit()
            # print(Tree.state_to_string(self, temp_board))
            print('temp')
            print(Checkers.print_board(self, board=Tree.string_to_state(self, temp_board)))
            print(max_child.state)
            quit()
            print()
            if Tree.state_to_string(self, temp_board) == max_child.state:
                return move

        print('Failed to find move')

    def set_node_score(self, node):
        # print(node.state)
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

    def update_board(self, board, move):
        new_coords = Checkers.apply_translation(self, move)

        board[new_coords[0]][new_coords[1]] = board[move[0][0]][move[0][1]]
        for coord in move[2]:
            board = Checkers.remove_piece(self, coord, input_board=board)
        board = Checkers.remove_piece(self, move[0], input_board=board)
        board = Checkers.check_crowns(self, input_board=board)
        return board