class BlockState:
    def __init__(self,h_value, actions, position):
        self.obstacle = None
        self.cost = 0
        self.g_value = 0
        self.h_value = h_value
        self.allowed = True
        self.actions = actions  ## seems like not needed kept for now
        self.position = position
        self.root_path = []


class Queue:

    def __init__(self, list_type="stack", length=100):
        self.explore_list = []
        self.list_type = list_type
        self.top = -1
        self.bottom = 0
        self.length = length

    def push(self, node):
        if self.length - self.bottom + self.top % self.length == self.length -1:
            print("queue full")
            raise Exception("Sorry, queue full")
        self.top += 1
        self.explore_list.append(node)

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


def board(size: [], goal_state, obstacles):

    board_env = [[BlockState(0,0,(0,0)) for j in range(size[1])] for i in range(size[0])]
    row_val = 0
    col_val = 0
    for row in board_env:
        for col in row:
            h_value = abs((goal_state[0]- row_val)) + abs((goal_state[1]- col_val))
            ## actions can be calulated and seems like not needed kept for now
            actions = 4
            if (row_val,col_val) in ((0,0),(0,7),(7,0),(7,7)): #corner cells
                actions = 2
            elif row_val in(0,7) or col_val in (0,7): #edge cells
                actions = 3
            else:
                actions = 4
            board_env[row_val][col_val] = BlockState(h_value, actions, (row_val,  col_val))
            col_val += 1
        col_val = 0
        row_val += 1
    for obstactle in obstactles:
        for i in obstactle[1]:
            board_env[i[0]][i[1]].cost = obstactle[3]
            board_env[i[0]][i[1]].allowed = obstactle[2]
            board_env[i[0]][i[1]].obstacle = obstactle[0]

    row_val = 0
    col_val = 0

    for row in board_env:
        for col in row:
            if not board_env[row_val][col_val].allowed:
                if col_val -1 >= 0 and board_env[row_val][col_val - 1].allowed is True:
                    cost = board_env[row_val][col_val - 1].cost
                    board_env[row_val][col_val - 1].cost = cost + board_env[row_val][col_val].cost
                if col_val + 1 < 8 and board_env[row_val][col_val + 1].allowed is True:
                    cost = board_env[row_val][col_val + 1].cost
                    board_env[row_val][col_val + 1].cost = cost + board_env[row_val][col_val].cost
                if row_val -1 >= 0 and board_env[row_val - 1][col_val].allowed is True:
                    cost = board_env[row_val - 1][col_val - 1].cost
                    board_env[row_val - 1][col_val].cost = cost + board_env[row_val][col_val].cost
                if row_val + 1 < 8 and board_env[row_val + 1][col_val].allowed is True:
                    cost = board_env[row_val + 1][col_val - 1].cost
                    board_env[row_val + 1][col_val].cost = cost + board_env[row_val][col_val].cost
                #diagonal cells
                if row_val + 1 < 8 and col_val + 1 < 8 and board_env[row_val + 1][col_val + 1].allowed is True:
                    cost = board_env[row_val + 1][col_val + 1].cost
                    board_env[row_val + 1][col_val + 1].cost = cost + board_env[row_val][col_val].cost
                if row_val + 1 < 8 and col_val - 1 >= 0 and board_env[row_val + 1][col_val - 1].allowed is True:
                    cost = board_env[row_val + 1][col_val - 1].cost
                    board_env[row_val + 1][col_val - 1].cost = cost + board_env[row_val][col_val].cost
                if row_val - 1 >= 0 and col_val - 1 >= 0 and board_env[row_val - 1][col_val - 1].allowed is True:
                    cost = board_env[row_val - 1][col_val - 1].cost
                    board_env[row_val - 1][col_val - 1].cost = cost + board_env[row_val][col_val].cost
                if row_val - 1 >= 0 and col_val + 1 < 8 and board_env[row_val - 1][col_val + 1].allowed is True:
                    cost = board_env[row_val - 1][col_val - 1].cost
                    board_env[row_val - 1][col_val + 1].cost = cost + board_env[row_val][col_val].cost
            col_val += 1
        col_val = 0
        row_val += 1

    return board_env

def find_children(game_board, position):

    childerns = []
    if position[0] + 1 < 8 and game_board[position[0]+1][position[1]].allowed is True:
        childerns.append(game_board[position[0] + 1][position[1]])
    if position[0] - 1 >= 8 and game_board[position[0]+1][position[1]].allowed is True:
        childerns.append(game_board[position[0] - 1][position[1]])
    if position[1] - 1 >= 0 and game_board[position[0]][position[1] - 1].allowed is True:
        childerns.append(game_board[position[0]][position[1] - 1])
    if position[1] + 1 < 8 and game_board[position[0]][position[1] + 1].allowed is True:
        childerns.append(game_board[position[0]][position[1] + 1])

    return childerns



def a_star(game_board, inital_position, goal_state):

    path = []
    returned_path = []
    explore_list = Queue(list_type="priority_queue")
    explored_list = []
    if inital_position == goal_state:
        path.append(inital_position, game_board[inital_position[0]][inital_position[1]].cost)
        return path

    explored_list.append((inital_position, path))
    children = find_children(game_board, inital_position)
    for child in children:
        if child.position != inital_position:
            child.g_value = game_board[inital_position[0]][inital_position[1]].cost + child.cost
            child.root_path = [(inital_position, 0)]
            explore_list.push((child, (inital_position, 0)))
    path = [(inital_position, 0)]
    node = (game_board[inital_position[0]][inital_position[1]],path)


    while explore_list.top != explore_list.bottom:
        prev_node = node
        node = explore_list.pop()


        path_reset = True
        for child in children:

            if node[0].position == child.position:
                path_reset = False

        if path_reset:
            path = node[0].root_path
        try:
            tmp_list = [val[0] for val in explored_list]
            tmp_list.index(node[0].position)

        except:
            if node[0].position == goal_state:
                path.append((node[0].position, node[0].cost))
                returned_path = path
                break
            explored_list.append((node[0].position, path))
            path.append((node[0].position, node[0].cost))
            children = find_children(game_board, node[0].position)

            for child in children:
                child.g_value = child.cost + node[0].g_value

                if child.position != inital_position:
                    child.root_path = path
                    explore_list.push((child, path))

    return returned_path


knight_position = (0,0)
queen_position = (7,6)

obstactles = [("wild animals", [(1,1), (1,2), (4,6), (4,7)], False, 5),
              ("fire", [(2,3), (2,4), (4,1)], False, 5),
              ("forrest", [(6,1), (6,2), (6,5), (7,5)], False, -5),
              ("water", [(0,4), (0,5), (3,0), (3,1)], False, -5),
              ("mountains", [(1,5), (1,6)], False, 3),
              ]

board_env = board([8,8], queen_position, obstactles)

board_env[knight_position[0]][knight_position[1]].obstacle='K'
board_env[queen_position[0]][queen_position[1]].obstacle='Q'

print("cost, obstacle, h_value, actions, position")
for i in board_env:
    for j in i:
        if j.cost < 0 and j.h_value>9:
            print(" {0}/{1}/{2}/{3}/{4}/{5} ".format(j.allowed, j.cost, j.obstacle or " ", j.h_value, j.actions, j.position), end = "|")
        elif j.cost < 0:
            print(" {0}/{1}/{2}/{3}/{4}/{5}  ".format(j.allowed, j.cost, j.obstacle or " ", j.h_value, j.actions, j.position), end = "|")
        elif j.h_value>9:
            print("  {0}/{1}/{2}/{3}/{4}/{5} ".format(j.allowed, j.cost, j.obstacle or " ", j.h_value, j.actions, j.position), end = "|")
        else:
            print("  {0}/{1}/{2}/{3}/{4}/{5}  ".format(j.allowed, j.cost, j.obstacle or " ", j.h_value, j.actions, j.position), end = "|")
    print("")

path = a_star(board_env, knight_position, queen_position)
print(path)
total_cost = 0
for i in path:
    total_cost += i[1]
print(total_cost)





