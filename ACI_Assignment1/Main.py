class BlockState:
    def __init__(self,h_value, actions, position):
        self.obstacle = None
        self.cost = 1
        self.h_value = h_value
        self.actions = actions  ## seems like not needed kept for now
        self.position = position

class Queue:

    def __init__(self, list_type="stack", length=100):
        self.explore_list = [None for i in range(length)]
        self.list_type = list_type
        self.top = 0
        self.bottom = 0
        self.length = length

    def push(self, node):
        if self.length - self.bottom + self.top % self.length == self.length -1:
            print("queue full")
            raise Exception("Sorry, queue full")
        self.explore_list[self.top] = node
        self.top += 1

    def pop(self):
        node = None
        if self.list_type == "stack":
            node = self.explore_list[self.top - 1]
            self.top -= 1
        else:
            if self.top == self.bottom:
                print("empty queue")
                raise Exception("Sorry, empty queue")
            min_value = 999
            for nd in explore_list:
                if nd.h_value < min_value:
                    min_value = nd.h_value
                    node = nd

            self.bottom += 1
        return node


def board(size: [], goal_state):

    board_env = [[BlockState(0,0,0) for j in range(size[1])] for i in range(size[0])]
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

    #wild animals
    board_env[1][1].cost = 5
    board_env[1][2].cost = 5
    board_env[4][6].cost = 5
    board_env[4][7].cost = 5
    board_env[1][1].obstacle = 'A'
    board_env[1][2].obstacle = 'A'
    board_env[4][6].obstacle = 'A'
    board_env[4][7].obstacle = 'A'
    #fire
    board_env[2][3].cost = 5
    board_env[2][4].cost = 5
    board_env[4][1].cost = 5
    board_env[2][3].obstacle = 'F'
    board_env[2][4].obstacle = 'F'
    board_env[4][1].obstacle = 'F'
    #forrest
    board_env[6][1].cost = -5
    board_env[6][2].cost = -5
    board_env[6][5].cost = -5
    board_env[7][5].cost = -5
    board_env[6][1].obstacle = 'J'
    board_env[6][2].obstacle = 'J'
    board_env[6][5].obstacle = 'J'
    board_env[7][5].obstacle = 'J'
    #water
    board_env[0][4].cost = -5
    board_env[0][5].cost = -5
    board_env[3][0].cost = -5
    board_env[3][1].cost = -5
    board_env[0][4].obstacle = 'W'
    board_env[0][5].obstacle = 'W'
    board_env[3][0].obstacle = 'W'
    board_env[3][1].obstacle = 'W'
    #mountains
    board_env[1][5].cost = 3
    board_env[1][6].cost = 3
    board_env[1][5].obstacle = 'M'
    board_env[1][6].obstacle = 'M'

    return board_env





knight_position = [0,0]
queen_position = [7,6]

board_env = board([8,8], queen_position)

board_env[knight_position[0]][knight_position[1]].obstacle='K'
board_env[queen_position[0]][queen_position[1]].obstacle='Q'

print("cost, obstacle, h_value, actions, position")
for i in board_env:
    for j in i:
        if j.cost < 0 and j.h_value>9:
            print(" {0}/{1}/{2}/{3}/{4} ".format(j.cost, j.obstacle or " ", j.h_value, j.actions, j.position), end = "|")
        elif j.cost < 0:
            print(" {0}/{1}/{2}/{3}/{4}  ".format(j.cost, j.obstacle or " ", j.h_value, j.actions, j.position), end = "|")
        elif j.h_value>9:
            print("  {0}/{1}/{2}/{3}/{4} ".format(j.cost, j.obstacle or " ", j.h_value, j.actions, j.position), end = "|")
        else:
            print("  {0}/{1}/{2}/{3}/{4}  ".format(j.cost, j.obstacle or " ", j.h_value, j.actions, j.position), end = "|")
    print("")

explore_list = Queue()

explore_list.push(board_env[0][0])
explore_list.push(board_env[0][1])
explore_list.push(board_env[7][6])

element = explore_list.pop()
print(element.h_value)
print(explore_list.top)
element = explore_list.pop()
print(element.h_value)
print(explore_list.top)



