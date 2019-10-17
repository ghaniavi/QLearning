import random
import numpy as np

# Open dataset
def open_dataset():
    data = np.genfromtxt("Data.txt")[::-1]
    return data
#  Create Q matrix
def create_qmatrix():
    q_matrix = []
    for i in range(15):
        q_matrix.append([[0 for j in range(4)] for k in range(15)])
    return q_matrix

# Create Environment matrix
def create_environment_matrix(dataset):
    environment_matrix = []
    for i in range(len(dataset)):
        data = []
        for j in range(len(dataset)):
            heading = []
            for k in range(4):
                if (k == 0):
                    if (i == 0):
                        heading.append(None)
                    else:
                        heading.append(int(dataset[i - 1][j]))
                if (k == 1):
                    if (i == 14):
                        heading.append(None)
                    else:
                        heading.append(int(dataset[i + 1][j]))
                if (k == 2):
                    if (j == 0):
                        heading.append(None)
                    else:
                        heading.append(int(dataset[i][j - 1]))
                if (k == 3):
                    if (j == 14):
                        heading.append(None)
                    else:
                        heading.append(int(dataset[i][j + 1]))
            data.append(heading)
        environment_matrix.append(data)
    return environment_matrix

# Find the possible next move from the current state
def possible_NextAct(cur_pos):
    step = [a != None for a in cur_pos]
    move = []
    if (step[0]):
        move.append(0)
    if (step[1]):
        move.append(1)
    if (step[2]):
        move.append(2)
    if (step[3]):
        move.append(3)
    return move

# Move current state to the next state by movement value
def nextState(cur_pos_data, move):
    nex_pos_data = [0]*2
    nex_pos_data[0] = cur_pos_data[0]
    nex_pos_data[1] = cur_pos_data[1]
    if (move == 0):
        nex_pos_data[1] -= 1
    elif (move == 1):
        nex_pos_data[1] += 1
    elif (move == 2):
        nex_pos_data[0] -= 1
    elif (move == 3):
        nex_pos_data[0] += 1
    return nex_pos_data

# find the maximum index from Q matrix
def maxindex(q_matrix, a, b):
    index_max = 0
    for i in range(4):
        if (q_matrix[a][b][i] != 0 and q_matrix [a][b][i] > q_matrix[a][b][index_max]):
            index_max = i
    return index_max

# Find the optimum path by the maximum index from Q matrix
# and the Total reward from the state
def findOptimumPath(q_matrix):
    heading = []
    current_position = [0,0]
    point = 0
    while (current_position != win_state):
        move = maxindex(q_matrix, current_position[1], current_position[0])
        point += environment_matrix[current_position[1]][current_position[0]][move]

        if (move == 0):
            heading.append("Up")
        if (move == 1):
            heading.append("Down")
        if (move == 2):
            heading.append("Left")
        if (move == 3):
            heading.append("Right")

        current_position = nextState(current_position, move)

        print("Total Reward : ", point)
    return heading

if __name__ == '__main__':
    dataset = open_dataset()
    q_matrix = create_qmatrix()
    environment_matrix = create_environment_matrix(dataset)
    learning_rate = 1
    discount_rate = 1

    for i in range(1000):
        x = random.choice(range(0, 15))
        y = random.choice(range(0, 15))
        current_position = [x, y]
        win_state = [14, 14]
        while(current_position != win_state):
            current_e_matrix = environment_matrix[current_position[1]][current_position[0]]
            possible_move = possible_NextAct(current_e_matrix)
            move = random.choice(possible_move)
            next_state = nextState(current_position, move)
            q_matrix[current_position[1]][current_position[0]][move] = q_matrix[current_position[1]][current_position[0]][move] + learning_rate * (environment_matrix[current_position[1]][current_position[0]][move] +discount_rate * max(q_matrix[next_state[1]][next_state[0]]) - q_matrix[current_position[1]][current_position[0]][move])
            current_position = next_state
        print("episode : ", i)
    heading = findOptimumPath(q_matrix)
    print("Movement : ", heading)



