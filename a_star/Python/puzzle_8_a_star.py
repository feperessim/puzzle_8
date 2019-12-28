import heapq

class PriorityQueue:
    def __init__(self):
        self.elements =[]

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

    def length(self):
        return len(self.elements)

class Node():
    def __init__(self, board=[]):
        self.board = board
        self.adjacency_list = []
        self.cost = 0
        self.parent = None

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(str(self.board))

    def __lt__(self, other):
        return h(self.board) + self.cost < h(other.board) + self.cost

        
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
                self.add_item_to_adjacency_list(Node(adj_list))
                
root_node = Node([[2, 6, 0],
                 [5, 7, 3],
                 [8, 1, 4]])

goal_node = Node([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 0]])

def h(root_board, goal_board=goal_node.board):
    '''
    Calculates the manhattan distance
    given two boards and the formula: 
    |x1 - x2| + |y1 - y2|.
    input: root_board -- 2d list of integers
    to be calculated the manhattan distance.
    goal_board -- 2d list of integers
    used to calculated the manhattan distance.
    return: sum(distances) -- return the manhattan
    distance of the root_board.
    '''

    distances = []
    empty_cell = 0
    x1 = 0
    
    while x1 < 3:
        y1 = 0
        while y1 < 3:
            value = root_board[x1][y1]
            if value != empty_cell:
                row = None
                for r in goal_board:
                    if value in r:
                        row = r
                        break
                x2 = goal_board.index(row)
                y2 = row.index(value)
                distance = abs(x1 - x2) + abs(y1 - y2)
                distances.append(distance)
            y1 += 1
        x1 += 1
    return sum(distances)

def hamming_distance(board):
    distance = 0
    i = 0
    flatten = sum(board, [])

    for element in flatten:
        if element != 0 and element != (i + 1):
            distance += 1
        i += 1
    return distance
    
def showBoards(boards):
    count = 1
    for board in boards:
        for row in board:
            for col in row:
                print(col, " ", end='')
            print('\n')
        print('\n\n\n')

def a_star_search(root_node, goal_node):
    '''
    Implementation of the A*
    path find algorithm.
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

    frontier = PriorityQueue()
    frontier.put(root_node, 0)
    came_from = {}
    cost_so_far = {}
    came_from[root_node] = None
    cost_so_far[root_node] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal_node:
            break

        current.generate_adjacency_list()
        for children in current.get_adjacency_list():
            new_cost = cost_so_far[current] + 1
            if children not in cost_so_far or new_cost < cost_so_far[children]:
                cost_so_far[children] = new_cost
                priority = new_cost + h(children.get_board(), goal_node.get_board())
                frontier.put(children, priority)
                came_from[children] = current
                children.parent = current
        print("Nível: ", cost_so_far[current] + 1)
        print("Nodos: ", frontier.length())

    return came_from, cost_so_far

def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current.board)
        current = came_from[current]
    path.append(start.board) # optional
    path.reverse() # optional
    return path

import time

start = time.time()
came_from, _ = a_star_search(root_node, goal_node)
end = time.time()
print('\nTempo de execução em segundos: ', end - start, '\n')
boards = reconstruct_path(came_from, root_node, goal_node)
showBoards(boards)
print(len(boards))
