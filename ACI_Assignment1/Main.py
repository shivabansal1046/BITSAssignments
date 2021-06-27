class block_state:
    def __init__(self):
        self.obstacle = None
        self.cost = 0
        self.h_value = 9999


def board(size: []):

    board_env = [[block_state() for j in range(size[1])] for i in range(size[0])]
    #wild animals
    board_env[1][1].cost = -5
    board_env[1][2].cost = -5
    board_env[4][6].cost = -5
    board_env[4][7].cost = -5
    board_env[1][1].obstacle = 'A'
    board_env[1][2].obstacle = 'A'
    board_env[4][6].obstacle = 'A'
    board_env[4][7].obstacle = 'A'
    #fire
    board_env[2][3].cost = -5
    board_env[2][4].cost = -5
    board_env[4][1].cost = -5
    board_env[2][3].obstacle = 'F'
    board_env[2][4].obstacle = 'F'
    board_env[4][1].obstacle = 'F'
    #forrest
    board_env[6][1].cost = 5
    board_env[6][2].cost = 5
    board_env[6][5].cost = 5
    board_env[7][5].cost = 5
    board_env[6][1].obstacle = 'J'
    board_env[6][2].obstacle = 'J'
    board_env[6][5].obstacle = 'J'
    board_env[7][5].obstacle = 'J'
    #water
    board_env[0][4].cost = 5
    board_env[0][5].cost = 5
    board_env[3][0].cost = 5
    board_env[3][1].cost = 5
    board_env[0][4].obstacle = 'W'
    board_env[0][5].obstacle = 'W'
    board_env[3][0].obstacle = 'W'
    board_env[3][1].obstacle = 'W'
    #mountains
    board_env[1][5].cost = -3
    board_env[1][6].cost = -3
    board_env[1][5].obstacle = 'M'
    board_env[1][6].obstacle = 'M'

    return board_env

def calculate_hvalue(board_env, goal_state):
    row_val = 0
    col_val = 0
    for row in board_env:
        for col in row:
            board_env[row_val][col_val].h_value = abs((goal_state[0]- row_val)) + abs((goal_state[1]- col_val))
            col_val += 1
        col_val = 0
        row_val += 1
    return board_env


knight_position = [0,0]
queen_position = [7,6]

board_env = board([8,8])

knight_position = [0,0]
queen_position = [7,6]
board_env[knight_position[0]][knight_position[1]].obstacle='K'
board_env[queen_position[0]][queen_position[1]].obstacle='Q'

board_env = calculate_hvalue(board_env, queen_position)

for i in board_env:
    for j in i:
        if j.cost < 0 and j.h_value>9:
            print(" {0}/{1}/{2} ".format(j.cost, j.obstacle or " ", j.h_value), end = "|")
        elif j.cost < 0:
            print(" {0}/{1}/{2}  ".format(j.cost, j.obstacle or " ", j.h_value), end = "|")
        elif j.h_value>9:
            print("  {0}/{1}/{2} ".format(j.cost, j.obstacle or " ", j.h_value), end = "|")
        else:
            print("  {0}/{1}/{2}  ".format(j.cost, j.obstacle or " ", j.h_value), end = "|")
    print("")


