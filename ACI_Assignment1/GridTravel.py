#!/usr/bin/env python
# coding: utf-8

# # ACI Assignment 1: Grid Travel Agent
# 
# ### Assignment Group 12
# 
# 
#  | Name | Student ID | 
#  | :- | :- |  
#  | Shiva Bansal | 2020FC04280 | 
#  | Ashish Kumar Singh | 2020FC04285 | 
#  | Ashish Kumar Verma | 2020FC04142 | 
#  | Ganesh P S | 2020FC04024 | 
#  | Deepam Patel | 2020FC04141 | 
# 

# ### Assumptions:
# 
# 1.	Knight can move only one block at a time.
# 2.	Knight can move to UP, DOWN, LEFT and RIGHT but not DIAGONALLY.
# 3.	Knight is not allowed to pass through any of the obstacles. (To allow pass through any obstacle, the obstacles object needs to set "allowed" value to 'True')
# 4.	Assuming obstacle points in reverse order
#     *	5 reward points – 	Knight passes near Water or Forest
#     *	5 penalty points –	Knight passes near Fire or Wild Animals 
#     *	3 penalty points –	Knight passes near Mountain Terrain 
# 5.	The points will be considered for calculation for each obstacle which are at UP, DOWN, LEFT, RIGHT but not DIAGONALLY position to knight for each move.
# 6.	There is no reward or penalty for a block not surrounded by any of the obstacles.
# 7.	The grid size is fixed to 8 by 8. If this needs to change, update variables board_xmax and board_ymax
# 

# #### Data structures

# In[1]:


# Defines each cell/ block state of the board
class Cell:
    
    # Initializer function
    def __init__(self, h_value,  position):
        # cell has any obstacles like wild animal or forest
        self.obstacle = None
        # cost to visit the cell if value is negative then reward is associated
        self.cost = 0
        # cost from initial state/root which keeps on updated as agent visits the cell
        self.g_value = 0
        # Heuristic value user by inform search algorithm like A*
        self.h_value = h_value
        # Is it allowed to visit
        self.allowed = True
        # path initial state/root which keeps on updated as agent visits the cell
        self.root_path = None
        # position of cell on game board
        self.position = position
        # If already explored in to be explore list. As one cell can have many parent cells
        self.explored = False

    # Return the object position when print function is called on the object
    def __repr__(self):
        return "{}".format(self.position)

    # Return the object position when stsr function is called on the object
    def __str__(self):
        return "{}".format(self.position)


# In[2]:


# Queue class is priority queue which holds blocks/cells to be explored.
# Takes size of the queue and queue type. Stack and priority queues are supported
class Queue:

    # Initializer function
    def __init__(self, list_type="stack", length=100):
        self.explore_list = []
        self.list_type = list_type
        self.top = 0
        self.bottom = 0
        self.length = length

    # Function to push the node/cell to queue
    # Takes contant time as it simply puts element at the top of the queue
    def push(self, node):
        if self.length - self.bottom + self.top % self.length == self.length -1:
            print("queue full")
            raise Exception("Sorry, queue full")
        self.top += 1
        self.explore_list.append(node)

    # Return element which has minimum cost i.e. f value
    # fvalue = hvalue + gvalue.
    # Runs with O(n) time complexity as it finds value with minimum f value for all of n elements
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
                # Calculate the f_value
                f_value = self.explore_list[i][0].h_value + self.explore_list[i][0].g_value
                # Reset the minimum value if current f_value is lesser
                if f_value < min_value:
                    min_value = f_value
                    node = self.explore_list[i]
                    node_index = i

            new_list = []

            for i in range(self.top):
                if i != node_index:
                    new_list.append(self.explore_list[i])
            self.explore_list = new_list
            self.top = len(self.explore_list)

        return node


# #### Heuristic function

# In[3]:


# Return Manhattan distance between two points
def manhattan_distance(a, b):
      return (abs(a[0] - b[0]) + abs(a[1] - b[1]))

# Return Euclidean distance between two points
def euclidean_distance(a, b):
      return sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# This function estimates the Heuristic value for each cell state
# It estimates heuristic value using manhattan distance. This function at the cost O(m*n) 
# where m and n are rows and columns of the game board respectively
def h_func(game_board, goal_state):

    for row_val, row in enumerate(board_env):
        for col_val, col in enumerate(row):
            game_board[row_val][col_val].h_value = manhattan_distance(goal_state, (row_val, col_val))

    return game_board


# #### Initializing the board environment

# In[4]:


# Defines game board configuration
# Expects size as [rows, cols], 
# obstacles i.e. [("obstacle type", [cell positions], "allowed to be visited", cost)]
# Example ("wild animals", [(1,1), (1,2), (4,6), (4,7)], False, 5)
# This function runs at the worst cost of O(m*n)
# where m and n are rows and columns of the game board respectively

def board(size: [], obstacles):

    # Initialize the board
    board_env = [[Cell(0, (i,j)) for j in range(size[1])] for i in range(size[0])]

    for obstacle_name, obstacle_locations, obstacle_passthrough, obstacle_cost in obstacles:
        for x, y in obstacle_locations:
            board_env[x][y].cost = obstacle_cost
            board_env[x][y].allowed = obstacle_passthrough
            board_env[x][y].obstacle = obstacle_name
            # cell 1 left to obstacle
            if y - 1 >= 0 and board_env[x][y - 1].allowed:
                board_env[x][y - 1].cost += obstacle_cost
            # cell 1 right to obstacle
            if y + 1 < board_ymax and board_env[x][y + 1].allowed:
                board_env[x][y + 1].cost += obstacle_cost
            # cell 1 above to obstacle
            if x - 1 >= 0 and board_env[x - 1][y].allowed:
                board_env[x - 1][y].cost += obstacle_cost
            # cell 1 below to obstacle
            if x + 1 < board_xmax and board_env[x + 1][y].allowed:
                board_env[x + 1][y].cost += obstacle_cost
            #diagonal cells
            if x + 1 < board_xmax and y + 1 < board_ymax and board_env[x + 1][y + 1].allowed:
                board_env[x + 1][y + 1].cost += obstacle_cost
            if x + 1 < board_xmax and y - 1 >= 0 and board_env[x + 1][y - 1].allowed:
                board_env[x + 1][y - 1].cost += obstacle_cost
            if x - 1 >= 0 and y - 1 >= 0 and board_env[x - 1][y - 1].allowed:
                board_env[x - 1][y - 1].cost += obstacle_cost
            if x - 1 >= 0 and y + 1 < board_ymax and board_env[x - 1][y + 1].allowed:
                board_env[x - 1][y + 1].cost += obstacle_cost

    return board_env


# #### Search algorithm and supporting functions

# In[5]:


# Finds cells/frontiers which are allowed to be vistied by the agent
# from current position. This function runs at the constant cost of O(4) 
# as maximum allowed moves are 4
def find_children(game_board, position):

    children = []
    if position[0] + 1 < board_xmax and game_board[position[0]+1][position[1]].allowed is True:
        children.append((position[0] + 1, position[1]))
    if position[0] - 1 >= 0 and game_board[position[0]-1][position[1]].allowed is True:
        children.append((position[0] - 1, position[1]))
    if position[1] - 1 >= 0 and game_board[position[0]][position[1] - 1].allowed is True:
        children.append((position[0], position[1] - 1))
    if position[1] + 1 < board_ymax and game_board[position[0]][position[1] + 1].allowed is True:
        children.append((position[0], position[1] + 1))

    return children


# In[6]:


# A* inform search algorithm implementation to
# find optimal path from initial state to goal state.
# Expects board configuration, initial state and goal state. Time complexity of this algorithm if O(b^△h)
# where b is average branching factor which is 2.5 and △h is difference between actual path and optimal solution i.e. 28-13=15
#for initial position (0,0) and goal position (7,6)
def a_star(game_board, inital_position, goal_state):

    path = ""
    iterations = 0
    frontiers = 0
    explore_list = Queue(list_type="priority_queue")
    explored_list = []

    if inital_position == goal_state:
        path = path + str(inital_position) + "|" + str(game_board[inital_position[0]][inital_position[1]].cost)
        return path

    explored_list.append((inital_position, path))
    children = find_children(game_board, inital_position)
    frontiers += len(children)
    for child in children:
        if child != inital_position:
            game_board[child[0]][child[1]].g_value = game_board[inital_position[0]][inital_position[1]].cost                                                     + game_board[child[0]][child[1]].cost
            game_board[child[0]][child[1]].root_path = str(inital_position) + "|" + str(0)
            explore_list.push((game_board[child[0]][child[1]], (inital_position, 0)))
    path = path + str(inital_position) + "|" + str(0)
    node = (game_board[inital_position[0]][inital_position[1]],path)

    while explore_list.top != explore_list.bottom:
        iterations += 1
        node = explore_list.pop()

        path_reset = True

        explored_flag = False
        for val in explored_list:
            if val[0] == node[0].position:
                explored_flag = True

        if not explored_flag:
            for child in children:

                if node[0].position == child:
                    path_reset = False

            if path_reset:
                path = node[0].root_path

            if node[0].position == goal_state:
                path = path + separator + str(node[0].position) + "|" + str(node[0].cost)
                returned_path = path
                break
            explored_list.append((node[0].position, path))

            path = path + separator + str(node[0].position) + "|" + str(node[0].cost)
            children = find_children(game_board, node[0].position)
            frontiers += len(children)
            for child in children:

                game_board[child[0]][child[1]].g_value = game_board[child[0]][child[1]].cost + node[0].g_value

                if child != inital_position and game_board[child[0]][child[1]].explored == False:
                    game_board[child[0]][child[1]].root_path = path
                    explore_list.push((game_board[child[0]][child[1]], path))
                    game_board[child[0]][child[1]].explored = True

    print("\nCode complexity:")
    print("Number of cells explored to find out optimal path: {0}".format(iterations))
    print("Average branching factor (b): {0}".format(frontiers/iterations))
    print("depth of the optimal path (d): {0}".format(len(path.split(separator)) - 1))
    return path


# #### Validation

# In[7]:


# Read position and check if it is within the board, and is not one of the obstacles
def get_input(pawn_type, default):

    repeat = True

    while(repeat):
        position = input("Enter {}'s position (default:{}): ".format(pawn_type, default))

        if position:
            vals = position.split(",")
            point = (int(vals[0]), int(vals[1]))
            if (point in obstacle_list):
                print("Position entered has an obstacle.")
            elif (point[0] < 0 or point[1] < 0 or point[0] > 7 or point[1] > 7):
                print("Invalid value entered. Please enter 0 <= x < {} and 0 <= y < {}.".format(board_xmax, board_ymax))
            else:
                repeat = False
        else:
            point = default
            repeat = False

    print ("{} position: {}".format(pawn_type, point))
    return point


# #### Board display functions

# In[8]:


# Function to return direction arrows based on previous and current positions
def get_direction(prev_x, prev_y, x, y):
    # Default return right
    direction = right
    if (prev_x != x):
        # prev_y != y only if diagonal movement allowed.
        if (prev_x < x):
            # Current is below previous
            direction = down
        else:
            # Current is above previous
            direction = up
    else:
        if (prev_y < y):
            # Current is to the left of previous
            direction = right
        else:
            # Current is to the right of previous
            direction = left
    
    return direction


# In[14]:


import ast
def parse_path(path):
    temp = path.split("|")
    #path_array = [ast.literal_eval(temp[0])]
    path_array = [eval(temp[0])]
    for i in temp[1:-1]:
        str_tuple = i.split("→")[1]
        path_array.append(ast.literal_eval(str_tuple.strip()))
    return path_array

def print_layout(board):
    print()
    n = board_xmax
    st = "   "
    for i in range(n):
        add = "  " if n%2==0 else ""
        st = st + "          " + str(i) + add
    print(st)   
 
    for r in range(n):
        st = "     "
        if r == 0:
            for col in range(n):
                st = st + "______________" 
            print(st)
 
        st = "     "
        for col in range(n):
            st = st + "|            "
        print(st + "|")
         
        st = "  " + str(r) + "  "
        for col in range(n):
            length = len(board[r][col].obstacle) if board[r][col].obstacle else 0
            text = board[r][col].obstacle if board[r][col].obstacle else ""
            l = int((12-length)/2)
            ri = 11 - length - l
            if ri==-1:
                add = ""
            else:
                add = " "
            st = st + "|" + " "*l+text + " "*ri+add
        print(st + "|") 
 
        st = "     "
        for col in range(n):
            st = st + "|____________"
        print(st + '|')
 
    print()


# #### Main function
# (Restart from this point for a new run)

# In[15]:


### Main code execution starts form here

# Program constants and inputs

# initializing the knight and queen position
knight_position = (0,0)
queen_position = (7,6)

# Board size
board_xmax = 8
board_ymax = 8

# Unicode characters for direction arrows
left = u"\u2190"
up = u"\u2191"
right = u"\u2192"
down = u"\u2193"

separator = " " + right + " "

# Obstacles in the game board configuration
# Format: [("obstacle type", [cell positions], "allowed to be visited", cost)]

obstacles = [("wild animals", [(1,1), (1,2), (4,6), (4,7)], False, 5),
              ("fire", [(2,3), (2,4), (4,1)], False, 5),
              ("forest", [(0,4), (0,5), (3,0), (3,1)], False, -5),
              ("water", [(6,1), (6,2), (6,5), (7,5)], False, -5),
              ("mountains", [(1,5), (1,6),(3,3),(3,4)], False, 3)
            ]

obstacle_list = []
for obstacle in obstacles:
    obstacle_list += obstacle[1]

# Get Knight position, or default
knight_position = get_input("Knight", knight_position)

# Get Queen position, or default
queen_position = get_input("Queen", queen_position)


# In[16]:


# board configuration
board_env = board([board_xmax,board_ymax], obstacles)

# Heuristic estimation for given board configuration

board_env = h_func(board_env, queen_position)
board_env[knight_position[0]][knight_position[1]].obstacle='K'
board_env[queen_position[0]][queen_position[1]].obstacle='Q'

print("Board initial layout:")
print_layout(board_env)


# In[17]:


# calculating optimal path from knight postion to queen position
path = a_star(board_env, knight_position, queen_position)

print("\nOptimal path for knight to reach queen:")
print(path)

path_array = parse_path(path)

prev_row = knight_position[0]
prev_col = knight_position[1]
for row, column in path_array[1:-1]:
    board_env[row][column].obstacle = get_direction(prev_row, prev_col, row, column)
    prev_row = row
    prev_col = column

print_layout(board_env)


# #### Cost calculation

# In[19]:


total_cost = 0
steps = 0
for i in path.split(separator):
    total_cost += int(i.split("|")[1])
    steps += 1

print("Number of steps needed: {0}".format(steps-1))

print("Total {}: {}".format("reward" if (total_cost < 0) else "cost", abs(total_cost)))


# In[ ]:




