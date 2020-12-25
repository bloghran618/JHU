import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
import yaml
from statistics import mean
import math

from board import Board
from utils import *

#Defining the different parameters
epsilon = 0.01
gamma = 0.9

# define the actions that the racecar can take (x and y acceleration components)
actions = [
    [-1, -1],
    [-1, 0],
    [-1, 1],
    [0, -1],
    [0, 0],
    [0, 1],
    [1, -1],
    [1, 0],
    [1, 1]
]

# board parameters
with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
track = config['track']
crash_behavior = config['crash_behavior']
outputfile = f'output/value-iteration-{track}-track-{crash_behavior}.output.txt'
clear_file_output(outputfile)
board = Board(track, crash_behavior, outputfile, verbose=False)

# determine the x, y coordinates of every space on the board that is not a wall
board_not_wall = []
for row_num, row in enumerate(board.board):
    for col_num, col in enumerate(row):
        if board.board[row_num][col_num] != '#':
            board_not_wall.append([col_num, row_num])
write_output(outputfile, 'valid board spaces:')
for loc in board_not_wall:
    write_output(outputfile, loc)
write_output(outputfile, f'the number of valid spaces on the board is: {len(board_not_wall)}')

# determine all valid states on the board (speed x<=abs(5), y<=abs(5))
states = []
for loc in board_not_wall:
    for x_acc in range(-5, 6):
        for y_acc in range(-5, 6):
            states.append([loc[0], loc[1], x_acc, y_acc])
write_output(outputfile, 'valid states:')
for state in states:
    write_output(outputfile, state)
write_output(outputfile, f'the number of valid states is: {len(states)}')

v_vals = [0 for _ in range(len(states))]
finish_locations = board.finish_locs
write_output(outputfile, f'the valid finish locations: {finish_locations}')

# update the values of the finish locations on the board
for v_index, v in enumerate(v_vals):
    state_loc = (states[v_index][1], states[v_index][0])
    if (state_loc) in finish_locations:
        v_vals[v_index] = board.finish_reward
write_output(outputfile, f'initial v values: \n{v_vals}')


def get_state_index(states, result_state):
    """
    for a given state return the index from the [states] array

    :param states: the [states] array
    :param result_state: the state to find the index of
    :return: the index of result_state in states
    """
    for state_index, state in enumerate(states):
        if state == result_state:
            return state_index
    raise RuntimeError

# initialize deltas to show learning progress
deltas = []

# increment the v values until minimal change
delta = epsilon + 1
learning_iteration = 0
while delta > epsilon:

    # track the previous v values so we can track learning
    v_vals_copy = v_vals.copy()

    # update the reward for each state
    for state_index, state in enumerate(states):
        max_reward = -math.inf

        # get the current state variables
        state_x = state[0]
        state_y = state[1]
        state_speed_x = state[2]
        state_speed_y = state[3]

        # get the reward if the acceleration attempt is unsuccessful
        failed_acc_state = board.get_action_result(state_x, state_y, state_speed_x, state_speed_y)
        if board.get_location_reward(failed_acc_state[0], failed_acc_state[1]) == board.finish_reward:
            failed_acc_reward = board.finish_reward
        else:
            failed_acc_index = get_state_index(states, failed_acc_state)
            failed_acc_reward = v_vals_copy[failed_acc_index]

        # iterate over each possible action
        for action in actions:

            # increment the speed for the action (ensure -5 <= speed <= 5)
            if abs(state_speed_x + action[0]) <= 5:
                action_speed_x = state_speed_x + action[0]
            else:
                action_speed_x = state_speed_x
            if abs(state_speed_y + action[1]) <= 5:
                action_speed_y = state_speed_y + action[1]
            else:
                action_speed_y = state_speed_y

            # get the reward if the acceleration attempt is successful
            completed_acc_state = board.get_action_result(state_x, state_y, action_speed_x, action_speed_y)
            if board.get_location_reward(completed_acc_state[0], completed_acc_state[1]) == board.finish_reward:
                completed_acc_reward = board.finish_reward
            else:
                completed_acc_index = get_state_index(states, completed_acc_state)
                completed_acc_reward = v_vals_copy[completed_acc_index]

            # compute the reward of the chosen action
            action_reward = 0.8 * completed_acc_reward + 0.2 * failed_acc_reward

            # get the highet reward value and assign it to the state reward via discount factor
            if action_reward > max_reward:
                max_reward = action_reward

        # update the v values if there is a better path found
        if v_vals_copy[state_index] < max_reward * gamma:
            v_vals[state_index] = max_reward * gamma
        else:
            v_vals[state_index] = v_vals_copy[state_index]

    # show the incrementation of the v values
    write_output(outputfile, f'old v values:')
    write_output(outputfile, v_vals_copy)
    write_output(outputfile, f'new v values:')
    write_output(outputfile, v_vals)

    # increment the learning iteration and check if we met our epsilon threshold
    learning_iteration += 1
    delta = 0
    for v_val_index, v_val in enumerate(v_vals):
        delta += abs(v_vals[v_val_index] - v_vals_copy[v_val_index])
    write_output(outputfile, f'delta from learning iteration {learning_iteration} is: {delta}')
    deltas.append(delta)

# output the v values
write_output(outputfile, f'the final v values:')
for v_index, v in enumerate(v_vals):
    write_output(outputfile, f'{states[v_index]} has v value {v}')

# demonstration of learned results and state-action-state tuples
board = Board(track, crash_behavior, outputfile, verbose=True)
test_board = Board(track, crash_behavior, outputfile, verbose=False)
episode_reward = 0
reward = -1
sas_tuples = []

while reward < 0:

    state = board.get_state_array()

    # get the current state variables
    state_x = state[0]
    state_y = state[1]
    state_speed_x = state[2]
    state_speed_y = state[3]

    # get the reward if the acceleration attempt is unsuccessful
    failed_acc_state = test_board.get_action_result(state_x, state_y, state_speed_x, state_speed_y)
    failed_acc_index = get_state_index(states, failed_acc_state)
    failed_acc_reward = v_vals[failed_acc_index]

    max_reward = -math.inf

    # iterate over each possible action
    for action in actions:

        # increment the speed for the action (ensure -5 <= speed <= 5)
        if abs(state_speed_x + action[0]) <= 5:
            action_speed_x = state_speed_x + action[0]
        else:
            action_speed_x = state_speed_x
        if abs(state_speed_y + action[1]) <= 5:
            action_speed_y = state_speed_y + action[1]
        else:
            action_speed_y = state_speed_y

        # get the reward if the acceleration attempt is successful
        completed_acc_state = test_board.get_action_result(state_x, state_y, action_speed_x, action_speed_y)
        completed_acc_index = get_state_index(states, completed_acc_state)
        completed_acc_reward = v_vals[completed_acc_index]

        # compute the reward of the chosen action
        action_reward = 0.8 * completed_acc_reward + 0.2 * failed_acc_reward

        # choose the highest reward value
        if action_reward > max_reward:
            max_reward = action_reward
            best_action = action

    # take the action and store the state-action-state tuple
    write_output(outputfile, f'the chosen action is {best_action} with expected reward {max_reward}')
    board.take_action(best_action[0], best_action[1])
    next_state = board.get_state_array()
    sas_tuples.append((state, action, next_state))
    state = next_state
    reward = board.get_reward()
    episode_reward += reward

# output the state-action-state tuples as well as the number of moves the demonstration took
write_output(outputfile, f'the state-action-state tuples:')
for tup in sas_tuples:
    write_output(outputfile, tup)
write_output(outputfile, f'the demonstration took {board.finish_reward - episode_reward + 1} moves')

# plot the learning of the course
plt.plot(deltas)
plt.ylabel('total change in v_values')
plt.xlabel('epoch')
plt.title(f'Value Iteration Learning Progress on Track {track} with {crash_behavior}')
plt.show()
