class Node():
    def __init__(self, board=[]):
        self.board=board
        self.adjacency_list=[]
        
    def get_adjacency_list(self):
        return self.adjacency_list

    def set_adjacency_list(self, adjacency_list):
        self.adjacency_list = adjacency_list

    def add_item_to_adjacency_list(self, item):
        self.adjacency_list.append(item)

    def get_board(self):
        return self.board

    def generate_adjacency_list(self):
        '''
        Generates the adjancency list
        from a given puzzle 8's board.
        '''
        # adj_lists = []
        empty_cell = 0
        row_empty_cell = col_empty_cell = 0
        tmp_array = None
        
        for array in self.board:
            if empty_cell in array:
               tmp_array = array
               break
        row_empty_cell = self.board.index(tmp_array)
        col_empty_cell = tmp_array.index(empty_cell)

        left = (row_empty_cell, col_empty_cell - 1)
        right = (row_empty_cell, col_empty_cell + 1)
        up = (row_empty_cell - 1, col_empty_cell)
        down = (row_empty_cell + 1, col_empty_cell)
        max_bound = 3

        for direction in [left, up, right, down]:
            (row, col) = direction
            if row >= 0 and row < max_bound and col >= 0 and col < max_bound:
                adj_list = [r[:] for r in self.board]
                adj_list[row_empty_cell][col_empty_cell] = adj_list[row][col]
                adj_list[row][col] = empty_cell
                #if self.has_solution(adj_list):
                self.add_item_to_adjacency_list(Node(adj_list))
        #self.set_adjacency_list(adj_lists)

    def has_solution(self, bo):
        count = 0
        board = sum(bo, [])
        for a in board:
            for b in board:
                if a > b:
                    count += 1
        return count % 2 == 0
    

def bfs(root_node, goal_node):
    '''
    Implementation of the Breadth
    First Search algorithm.
    The problem to be solved by this
    algorithm is the Puzzle 8 game.

    input: root_node -- the root node where
    the search begins.
    goal_node -- The objective to reach.
    
    return:
    (path, node) -- A tuple with a
    dictionary path whose key node
    gives the path backwards to the
    objective node.
    '''
    frontier = [root_node]
    path = {root_node : None} # The path where a node came from
    level = {root_node : 0}
    boards = set(str(root_node.get_board())) # List of boards to check a board was already generated
    i = 1
    while frontier:
        next_frontier = []
        for node_parent in frontier:
            if node_parent.get_board() == goal_node.get_board():
                return (path, node_parent)
            node_parent.generate_adjacency_list()
            for children in node_parent.get_adjacency_list():
                if str(children.get_board()) not in boards:
                    boards.add(str(children.get_board()))
                    next_frontier.append(children)
                    level[children] = i
                    path[children] = node_parent
        frontier = next_frontier
        print("Nível ", i)
        print("Qtd nodos ", len(frontier))
        i += 1
    return (path, root_node)

def showBoards(boards):
    count = 1
    for board in boards:
        for row in board:
            for col in row:
                print(col, " ", end='')
            print('\n')
        print('\n\n\n')


def to_matrix(l, n):
    '''
    Converts a list l into a matrix
    of size n x n.
    input:
    l -- a list of size 1 x m
    n -- integer to be the new dimension of 
    the resulting matrix
    return:
    returns a list of lists of size n x n
    '''
    return [l[i:i+n] for i in range(0, len(l), n)]

def genRandomBoard():
    '''
    Generates a random board 3x3
    '''
    board = [i for i in range(9)]
    random.shuffle(board)
    return to_matrix(board, 3)

def pathBackWards(path, node):
    '''
    Given a node and path it
    creates a list with the path backwards
    i.e. from the bottom to the top.
    '''
    u = node
    p = []
    while path[u] is not None:
        p.append(u.board)
        u = path[u]
    return p


root_node = Node([[2, 6, 0],
                 [5, 7, 3],
                 [8, 1, 4]])

unsolveable_node = Node([[1, 2, 3],
                         [4, 5, 6],
                         [8, 7, 0]])

goal_node = Node([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]])

import time

start = time.time()
path, node =  bfs(root_node, goal_node)
end = time.time()
print('\nTempo de execução em segundos: ', end - start, '\n')

p = pathBackWards(path, node)
p.append(root_node.board)
showBoards(p)
