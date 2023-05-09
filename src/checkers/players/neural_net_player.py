import sys, copy, time, random
sys.path.append('./src/checkers/blondie24')
from neural_net import *
from tree import *


class NeuralNetPlayer:
    def __init__(self, net=None):
        self.player_num = None
        self.net = net
        self.tree = None


    def choose_move(self, board, possible_moves):
        if not self.net: self.net = NeuralNet.create_net(self.player_num, 2)
        if not self.tree: self.tree = Tree(self.player_num)
        
        # s = time.time()
        self.tree.construct_tree(board)
        # print(f'constructed tree from move in: {round(time.time()-s, 4)}s')

        board_node = self.tree.states[Tree.state_to_string(self, board)]
        # s = time.time()
        self.set_node_scores(board_node)
        # print(f'scored nodes in: {round(time.time()-s, 4)}s')

        # s = time.time()
        max_child = board_node.children[0]
        for child in board_node.children:
            if child.score > max_child.score:
                max_child = child
        
        for move in possible_moves:
            temp_board = self.update_board(board, move)
            if Tree.state_to_string(self, temp_board) == max_child.state:
                # print(f'chose move in: {time.time()-s}s')
                return move

    def set_node_scores(self, node):
        stack = [node]
        visited_states = {node.state:node}

        while len(stack) != 0:
            current_node = stack[0]
            visited_states[current_node.state] = current_node

            # Node can be scored directly
            if len(current_node.children) == 0:
                if current_node.winner == self.player_num:
                    current_node.score = 1
                elif current_node.winner == 3 - self.player_num:
                    current_node.score = -1
                else:
                    # s = time.time()
                    # current_node.score = random.random()
                    current_node.score = self.net.get_net_output(Tree.string_to_state(self, node.state))
                    # print(f'net score time: {round(time.time()-s, 4)}')
                stack.pop(0)
                continue
            
            # Node can be scored by children
            children_scores = [child.score for child in current_node.children]
            if None not in children_scores:
                if current_node.player_num == self.player_num:
                    current_node.score = max(children_scores)
                else:
                    current_node.score = min(children_scores)
                stack.pop(0)
                continue
            
            unscored_children = []
            has_looping_children = False
            for child in current_node.children:
                if child.depth == None or child.depth < current_node.depth:
                    has_looping_children = True
                    # child.score = random.random()
                    child.score = self.net.get_net_output(Tree.string_to_state(self, child.state))
                elif child.score == None and child.state not in visited_states:
                    unscored_children.append(child)
            
            if has_looping_children:
                # current_node.score = random.random()
                current_node.score = self.net.get_net_output(Tree.string_to_state(self, current_node.state))
                stack.pop(0)
            
            for child in unscored_children:
                stack.insert(0, child)

    def update_board(self, board, move):
        updated_board = copy.deepcopy(board)
        new_coords = Checkers.apply_translation(self, move)

        updated_board[new_coords[0]][new_coords[1]] = updated_board[move[0][0]][move[0][1]]
        for coord in move[2]:
            updated_board = Checkers.remove_piece(self, coord, input_board=updated_board)

        updated_board = Checkers.remove_piece(self, move[0], input_board=updated_board)
        updated_board = Checkers.check_crowns(self, input_board=updated_board)
        return updated_board
