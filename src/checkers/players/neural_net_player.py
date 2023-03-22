import sys, copy
sys.path.append('./src/checkers/blondie24')
from neural_net import *
from tree import *


class NeuralNetPlayer:
    def __init__(self):
        self.player_num = None
        self.net = None
        self.tree = None


    def choose_move(self, board, possible_moves):
        if not self.net: self.net = NeuralNet.create_net(self.player_num, 2)
        if not self.tree: self.tree = Tree(self.player_num)

        self.tree.construct_tree(board)

        board_node = self.tree.states[Tree.state_to_string(self, board)]
        print('setting node scores...')
        self.set_node_scores(board_node)
        print('done\n')
        print([child.score for child in board_node.children])

        max_child = board_node.children[0]
        for child in board_node.children:
            if child.score > max_child.score:
                max_child = child
        
        for move in possible_moves:
            temp_board = self.update_board(board, move)
            if Tree.state_to_string(self, temp_board) == max_child.state:
                return move
        
        print('Failed to find move')
        quit()

    def p(self, state):
        Checkers.print_board(self, board=Tree.string_to_state(self, state))

    def set_node_scores(self, node):
        stack = [node]

        while len(stack) != 0:
            current_node = stack[0]

            # Node can be scored directly
            if len(current_node.children) == 0:
                if current_node.winner == self.player_num:
                    current_node.score = 1
                elif current_node.winner == 3 - self.player_num:
                    current_node.score = -1
                else:
                    current_node.score = self.net.get_net_output(Tree.string_to_state(self, node.state))
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
            
            has_looping_children = False
            looping_children_idxes = []
            for i, child in enumerate(current_node.children):
                if child.depth == None or child.depth < current_node.depth:
                    has_looping_children = True
                    looping_children_idxes.append(i)
                elif child.score == None and child not in stack:
                    stack.insert(0, child)
            
            if has_looping_children:
                current_node.score = self.net.get_net_output(Tree.string_to_state(self, node.state))
                stack.pop(0)



            # for i, child in enumerate(current_node.children):
            #     if i not in looping_children_idxes and child.score == None and child not in stack:
            #         stack.insert(0, child)


            
            

            


        
        
        
        
        
        return
        stack = [node]
        prev_len = [len(stack)]
        prev_node = None
        while len(stack) != 0:
            current_node = stack[0]
            print(f'current node: {current_node.idx}')

            # if current_node == prev_node:
            #     # print()
            #     # # print(len(stack))
            #     # print(current_node.children)
            #     # print([child.score for child in current_node.children])
            #     # print('current state')
            #     Checkers.print_board(self, board=Tree.string_to_state(self, current_node.state))
                # for child in current_node.children:
                #     if child.score == None:
                #         print('non scored child state')
                #         self.p(child.state)
                # print(current_node.player_num)
                # print(current_node.state)

            prev_len = len(stack)
            

            
            '''
            Current node either:
            Child of itself
            None child already in stack
            '''

            valid_children_len = len(current_node.children)
            children_to_check = []


            children_scores = [child.score for child in current_node.children]
            children_depths = [child.depth for child in current_node.children]

            has_only_looping_children = True
            for child in current_node.children:
                if child.depth > current_node.depth:
                    has_only_looping_children = False
                    if child.score == None:
                        stack.insert(0, child)

    


            
            
            # loop = False
            # for i in children_depths:
            #     if current_node.depth > i:
            #         loop = True

            # if loop:
            #     valid_children_len -= 1
    


            if not has_only_looping_children or len(current_node.children) == 0:
                # if current_node == prev_node: print('no children')
                if current_node.winner == self.player_num:
                    current_node.score = 1
                elif current_node.winner == 3 - self.player_num:
                    current_node.score = -1
                else:
                    current_node.score = self.net.get_net_output(Tree.string_to_state(self, node.state))
                stack.pop(0)

            elif has_only_looping_children or None not in children_scores:
                if current_node == prev_node: print('none not in children')
                if current_node.player_num == self.player_num:
                    current_node.score = max(children_scores)
                else:
                    current_node.score = min(children_scores)
                stack.pop(0)

            # else:
            #     for child in current_node.children:
            #         if child.score == None and child.depth > current_node.depth: #state not in [i.state for i in stack]:
            #             stack.insert(0, child)

            # else:
            #     for child in current_node.children:
                    
            #         if current_node == prev_node:
            #             if child.score == None:
            #                 print(f'child: {child.idx}')
            #                 print(f'depths:\ncurrent node: {current_node.depth}\nchild: {child.depth}')
            #                 # if child.state in [i.state for i in stack]:
            #                 #     print('child already in stack')
            #                 # if current_node.state in [j.state for j in child.children]:
            #                 #     print('current node is a child of its child')
            #         if child.score == None and child.depth > current_node.depth: #state not in [i.state for i in stack]:
            #             if current_node == prev_node: print('child added to stack')

            #             stack.insert(0, child)
            #         elif child.depth < current_node.depth:
                        
            

            
            print()
            prev_node = current_node


            
            




            

            
            
    #     #     for child in root_node.children:
    #     #     self.set_node_score(child)
    #     # return [child.score for child in root_node.children]
        
        
    #     if len(node.children) == 0:
    #         if node.winner == self.player_num:
    #             node.score = 1
    #         elif node.winner == 3 - self.player_num:
    #             node.score = -1
    #         else:
    #             node.score = self.net.get_net_output(Tree.string_to_state(self, node.state))
    #         return
        
    #     node.score = max(self.get_children_scores(node))
        
    # def get_children_scores(self, root_node):
    #     if len(root_node.children) == 0:
    #         return
    #     for child in root_node.children:
    #         self.set_node_score(child)
    #     return [child.score for child in root_node.children]

    def update_board(self, board, move):
        updated_board = copy.deepcopy(board)
        new_coords = Checkers.apply_translation(self, move)

        updated_board[new_coords[0]][new_coords[1]] = updated_board[move[0][0]][move[0][1]]
        for coord in move[2]:
            updated_board = Checkers.remove_piece(self, coord, input_board=updated_board)

        updated_board = Checkers.remove_piece(self, move[0], input_board=updated_board)
        updated_board = Checkers.check_crowns(self, input_board=updated_board)
        return updated_board