'''defines each cell/ block state of the board'''
class BlockState:
    def __init__(self, h_value,  position):
        self.obstacle = None # cell has any obstacle like wild animal or forrest
        self.cost = 0 # cost to visit the cell if value is negative then reward is associated
        self.g_value = 0 # cost from initial state/root which keeps on updated as agent visits the cell
        self.h_value = h_value # Heuristic value user by inform search algorithm like A*
        self.allowed = True # Is it allowed to visit
        self.root_path = None #path initial state/root which keeps on updated as agent visits the cell
        self.position = position ## position of cell on game board
        self.pushed = False # If already pushed in to be explore list. As one cell can have many parent cells

''' Queue class is priority queue which holds blocks/cell to be explored.
Takes size of the queue and queue type. Stack and priority queues are supported'''
class Queue:

    def __init__(self, list_type="stack", length=100):
        self.explore_list = []
        self.list_type = list_type
        self.top = 0
        self.bottom = 0
        self.length = length
    ''' pushes the node/cell to queue'''
    def push(self, node):
        if self.length - self.bottom + self.top % self.length == self.length -1:
            print("queue full")
            raise Exception("Sorry, queue full")
        self.top += 1
        self.explore_list.append(node)
    ''' Return element which has minimum cost i.e. f value
    fvalue = hvalue + gvalue'''
    def pop(self):
        node = None

        if self.list_type == "stack":
            node = self.explore_list[self.top - 1]
            self.top -= 1
        else:
            if self.top < 0:
                print("empty queue")
                raise Exception("Sorry, empty queue")
            min_value = 9999
            node_index = 0
            for i in range(self.top):
                if self.explore_list[i][0].h_value + self.explore_list[i][0].g_value < min_value:
                    min_value = self.explore_list[i][0].h_value + self.explore_list[i][0].g_value
                    node = self.explore_list[i]
                    node_index = i

            new_list = []

            for i in range(self.top):
                if i != node_index:
                    new_list.append(self.explore_list[i])
            self.explore_list = new_list
            self.top = len(self.explore_list)
        return node

''' This functions estimates the Heuristic value for each cell state
It estimates heuristic value using manhattan distance '''
def h_func(game_board, goal_state):
    row_val = 0
    col_val = 0
    for row in board_env:
        for col in row:
            h_value = abs((goal_state[0]- row_val)) + abs((goal_state[1]- col_val))
            game_board[row_val][col_val].h_value = h_value
            col_val += 1
        col_val = 0
        row_val += 1
    return game_board

'''Defines game board configuration expects 
size as [rows, cols], 
obstacles i.e. [("obstacle type", [cell positions], "allowed to be visited", cost)]
Example ("wild animals", [(1,1), (1,2), (4,6), (4,7)], False, 5)'''
def board(size: [], obstacles):

    board_env = [[BlockState(0,(0,0)) for j in range(size[1])] for i in range(size[0])]
    row_val = 0
    col_val = 0
    for row in board_env:
        for col in row:

            board_env[row_val][col_val] = BlockState(0,  (row_val,  col_val))
            col_val += 1
        col_val = 0
        row_val += 1
    for obstactle in obstactles:
        for pos in obstactle[1]:
            board_env[pos[0]][pos[1]].cost = obstactle[3]
            board_env[pos[0]][pos[1]].allowed = obstactle[2]
            board_env[pos[0]][pos[1]].obstacle = obstactle[0]
            # cell 1 left to obstacle
            if pos[1] -1 >= 0 and board_env[pos[0]][pos[1] - 1].allowed:
                board_env[pos[0]][pos[1] - 1].cost += obstactle[3]
            # cell 1 right to obstacle
            if pos[1] + 1 < 8 and board_env[pos[0]][pos[1] + 1].allowed:
                board_env[pos[0]][pos[1] + 1].cost += obstactle[3]
            # cell 1 above to obstacle
            if pos[0] - 1 >= 0 and board_env[pos[0] - 1][pos[1]].allowed:
                board_env[pos[0] - 1][pos[1]].cost += obstactle[3]
            # cell 1 below to obstacle
            if pos[0] + 1 < 8 and board_env[pos[0] + 1][pos[1]].allowed:
                board_env[pos[0] + 1][pos[1]].cost += obstactle[3]
            #diagonal cells
            if pos[0] + 1 < 8 and pos[1] + 1 < 8 and board_env[pos[0] + 1][pos[1] + 1].allowed:
                board_env[pos[0] + 1][pos[1] + 1].cost += obstactle[3]
            if pos[0] + 1 < 8 and pos[1] - 1 >= 0 and board_env[pos[0] + 1][pos[1] - 1].allowed:
                board_env[pos[0] + 1][pos[1] - 1].cost += obstactle[3]
            if pos[0] - 1 >= 0 and pos[1] - 1 >= 0 and board_env[pos[0] - 1][pos[1] - 1].allowed:
                board_env[pos[0] - 1][pos[1] - 1].cost += obstactle[3]
            if pos[0] - 1 >= 0 and pos[1] + 1 < 8 and board_env[pos[0] - 1][pos[1] + 1].allowed:
                board_env[pos[0] - 1][pos[1] + 1].cost += obstactle[3]

    return board_env

'''finds cells which are allowed to be vistied by the agent
 from current position'''
def find_children(game_board, position):

    childerns = []
    if position[0] + 1 < 8 and game_board[position[0]+1][position[1]].allowed is True:
        childerns.append((position[0] + 1, position[1]))
    if position[0] - 1 >= 0 and game_board[position[0]-1][position[1]].allowed is True:
        childerns.append((position[0] - 1, position[1]))
    if position[1] - 1 >= 0 and game_board[position[0]][position[1] - 1].allowed is True:
        childerns.append((position[0], position[1] - 1))
    if position[1] + 1 < 8 and game_board[position[0]][position[1] + 1].allowed is True:
        childerns.append((position[0], position[1] + 1))

    return childerns


''' A* inform search algorithm implementation to
find optimal path from initial state to goal state.
Expects board configuration, initial state and goal state'''
def a_star(game_board, inital_position, goal_state):

    path = ""
    explore_list = Queue(list_type="priority_queue")
    explored_list = []

    if inital_position == goal_state:
        path = path + str(inital_position) + "|" + str(game_board[inital_position[0]][inital_position[1]].cost)
        return path

    explored_list.append((inital_position, path))
    children = find_children(game_board, inital_position)

    for child in children:
        if child != inital_position:
            game_board[child[0]][child[1]].g_value = game_board[inital_position[0]][inital_position[1]].cost + game_board[child[0]][child[1]].cost
            game_board[child[0]][child[1]].root_path = str(inital_position) + "|" + str(0)
            explore_list.push((game_board[child[0]][child[1]], (inital_position, 0)))
    path = path + str(inital_position) + "|" + str(0)
    node = (game_board[inital_position[0]][inital_position[1]],path)

    while explore_list.top != explore_list.bottom:

        node = explore_list.pop()

        path_reset = True
        for child in children:

            if node[0].position == child:
                path_reset = False

        if path_reset:
            path = node[0].root_path

        explored_flag = False
        for val in explored_list:
            if val[0] == node[0].position:
                explored_flag = True

        if not explored_flag:
            if node[0].position == goal_state:
                path = path + " -> " + str(node[0].position) + "|" + str(node[0].cost)
                returned_path = path
                break
            explored_list.append((node[0].position, path))

            path = path + " -> " + str(node[0].position) + "|" + str(node[0].cost)
            children = find_children(game_board, node[0].position)

            for child in children:
                game_board[child[0]][child[1]].g_value = game_board[child[0]][child[1]].cost + node[0].g_value
                if child != inital_position and game_board[child[0]][child[1]].pushed == False:
                    game_board[child[0]][child[1]].root_path = path
                    explore_list.push((game_board[child[0]][child[1]], path))
                    game_board[child[0]][child[1]].pushed = True
    return path

''' main code execution starts form here
initializing the knight position and queen position'''
knight_position = (0,0)
queen_position = (7,6)
initial_position = input("enter Knight's position 0,0: ")
goal_position = input("enter Queen's position 7,6: ")
if(initial_position):
    init = initial_position.split(",")
    knight_position = (int(init[0]), int(init[1]))

if(goal_position):
    goal = goal_position.split(",")
    queen_position = (int(goal[0]), int(goal[1]))
    print(queen_position)


''' obstacle in the game board configuration
obstacles i.e. [("obstacle type", [cell positions], "allowed to be visited", cost)]'''

obstactles = [("wild animals", [(1,1), (1,2), (4,6), (4,7)], False, 5),
              ("fire", [(2,3), (2,4), (4,1)], False, 5),
              ("forrest", [(0,4), (0,5), (3,0), (3,1)], False, -5),
              ("water", [(6,1), (6,2), (6,5), (7,5)], False, -5),
              ("mountains", [(1,5), (1,6),(3,3),(3,4)], False, 3)
              ]
''' board configuration'''
board_env = board([8,8], obstactles)

''' Heuristic estimation for given board configuration'''

board_env = h_func(board_env, queen_position)
board_env[knight_position[0]][knight_position[1]].obstacle='K'
board_env[queen_position[0]][queen_position[1]].obstacle='Q'
''' Print board configuration as matrix of given size'''
print("cost, obstacle, h_value, actions, position")
for i in board_env:
    for j in i:
        if j.cost < 0 and j.h_value>9:
            print(" {0}/{1}/{2}/{3}/{4} ".format(j.allowed, j.cost, j.obstacle or " ", j.h_value,  j.position), end = "|")
        elif j.cost < 0:
            print(" {0}/{1}/{2}/{3}/{4}  ".format(j.allowed, j.cost, j.obstacle or " ", j.h_value,  j.position), end = "|")
        elif j.h_value>9:
            print("  {0}/{1}/{2}/{3}/{4} ".format(j.allowed, j.cost, j.obstacle or " ", j.h_value,  j.position), end = "|")
        else:
            print("  {0}/{1}/{2}/{3}/{4}  ".format(j.allowed, j.cost, j.obstacle or " ", j.h_value,  j.position), end = "|")
    print("")

''' calculating optimal path from knight postion to queen position'''
path = a_star(board_env, knight_position, queen_position)

print("\noptimal path for knight to reach queen")
print(path)

''' cost calculation'''
total_cost = 0
steps = 0
for i in path.split(" -> "):
    total_cost += int(i.split("|")[1])
    steps += 1

print("Number of steps needed: {0}".format(steps))

if total_cost < 0:
    print("Total reward: {0}".format(abs(total_cost)))
else:
    print("Total cost: {0}".format(total_cost))





















