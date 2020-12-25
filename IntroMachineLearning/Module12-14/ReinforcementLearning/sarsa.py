import numpy as np
from random import random, randint
import matplotlib.pyplot as plt
import yaml
from statistics import mean

from board import Board
from utils import *


#Defining the different parameters
epsilon = 0.9
total_episodes = 5000
alpha = 0.85
gamma = 0.95

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
outputfile = f'output/sarsa-{track}-track-{crash_behavior}.output.txt'
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

# initialize q values for all states and actions to 0
q_vals = np.zeros((len(states), len(actions)))



def choose_action(state, verbose):
    """
    choose an action for learning

    :param state: the current state (by index)
    :param verbose: whether to print output
    :return: the action to take (by index)
    """
    if random() > epsilon:
        # choose a random action 1-epsilon% of the time
        action = randint(0, 8)
        if verbose:
            write_output(outputfile, f'choose random action {actions[action]}')
    else:
        # choose the best action epsilon% of the time
        action = np.argmax(q_vals[state, :])
        if verbose:
            write_output(outputfile, f'choose best action {actions[action]}')
    return action


def choose_best_action(state):
    """
    choose the best action for completed learning demonstration purposes

    :param state: the current state (by index)
    :return: the action to take (by index)
    """
    action = np.argmax(q_vals[state, :])
    write_output(outputfile, f'choose best action {actions[action]}')
    return action


def learn(state, next_state, reward, action, next_action, verbose):
    """
    update the q values according to the sarsa algorithm

    :param state: the current state (by index)
    :param next_state: the chosen next state (by index)
    :param reward: the reward for the next state
    :param action: the action taken (by index)
    :param next_action: the next action to take (by index)
    :param verbose: whether to print output
    """
    predict = q_vals[state, action]
    target = reward + gamma * q_vals[next_state, next_action]
    if verbose:
        write_output(outputfile, f'current q vals at current state: {q_vals[state]}')
        write_output(outputfile, f'increment q val for action {actions[action]} (index {action}) by {alpha * (target - predict)}')
    q_vals[state, action] = q_vals[state, action] + alpha * (target - predict)
    if verbose:
        write_output(outputfile, f'new q vals for state: {q_vals[state]}')


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


# initialize the reward to 0 and an empty array for the moves by episode
cum_reward = 0
episode_reward = 0
moves = []

# play the game total_episodes times
for episode in range(total_episodes):
    write_output(outputfile, f'episode #{episode}')

    # only print detailed information for the first and last episodes
    if episode == 0 or episode == (total_episodes-1):
    # if episode == (total_episodes-1):
        verbose = True
    else:
        verbose = False

    # initialize the board and initial state
    board = Board(track, crash_behavior, outputfile, verbose=verbose)
    state = board.get_state_array()
    state_index = get_state_index(states, state)

    # choose an initial action
    action_index = choose_action(state_index, verbose)
    action = actions[action_index]
    reward = -1

    if verbose:
        write_output(outputfile, f'the chosen first action is: {action}')

    # continue until the learner reaches the result
    while reward < 0:

        # take the action chosen and get the new state
        board.take_action(action[0], action[1])
        next_state = board.get_state_array()
        if verbose:
            write_output(outputfile, f'the next state from the executed action is: {next_state}')
        next_state_index = get_state_index(states, next_state)

        # increment the reward by the reward value at the new location
        reward = board.get_reward()
        cum_reward += reward
        episode_reward += reward
        if verbose:
            write_output(outputfile, f'the reward so far is: {episode_reward}')

        # choose the next action
        next_action_index = choose_action(next_state_index, verbose)
        next_action = actions[next_action_index]

        # update the q values to learn the game
        learn(state_index, next_state_index, reward, action_index, next_action_index, verbose)

        # reset the state and action for the next learning iteration
        state_index = next_state_index
        action_index = next_action_index
        action = next_action

    # display the reward on the episode, update the moves by episode array, and reset the episode reward for the next episode
    write_output(outputfile, f'the reward on episode {episode} was {episode_reward}')
    moves.append(board.finish_reward - episode_reward + 1)
    episode_reward = 0

# display the q values
for row in q_vals:
    write_output(outputfile, row)

# write the average performance of the learner over all episodes
performance = cum_reward / total_episodes
write_output(outputfile, f'the average performance was: {performance}')


# demonstrate state action state for vehicle at end of learning
print('Demonstration of learned model:')
# initialize the reward, board and state-action-state tuples
episode_reward = 0
reward = -1
verbose = True
sas_tuples = []

# initialize the board, current state and initial action to take
board = Board(track, crash_behavior, outputfile, verbose=verbose)
state = board.get_state_array()
state_index = get_state_index(states, state)
action_index = choose_best_action(state_index)
action = actions[action_index]
while reward < 0:

    # take the selected action and get the state from the action
    board.take_action(action[0], action[1])
    next_state = board.get_state_array()
    if verbose:
        write_output(outputfile, f'the next state from the executed action is: {next_state}')
    next_state_index = get_state_index(states, next_state)

    # increment the reward by the reward value at the new location
    reward = board.get_reward()
    episode_reward += reward

    # keep track of the state-action-state tuples
    sas_tuples.append((states[state_index], action, next_state))

    # choose the best action and update the state and action for the next learning iteration
    next_action_index = choose_best_action(next_state_index)
    next_action = actions[next_action_index]
    state_index = next_state_index
    action_index = next_action_index
    action = next_action

# output the state-action-state tuples as well as the number of moves the demonstration took
write_output(outputfile, f'the state-action-state tuples:')
for tup in sas_tuples:
    write_output(outputfile, tup)
write_output(outputfile, f'the demonstration took {board.finish_reward - episode_reward + 1} moves')

# show the learning curve for the number of moves vs. episode number
moves_moving_avg = []
for index, move in enumerate(moves):
    if index < 10:
        first_n = moves[:(index+1)]
        moving_avg = mean(first_n)
        moves_moving_avg.append(moving_avg)
    else:
        # plot the last 10 episode moving average (because its smoother)
        first_n = moves[:index]
        prev_ten = first_n[-10:]
        moving_avg = mean(prev_ten)
        moves_moving_avg.append(moving_avg)
plt.plot(moves_moving_avg)
plt.ylabel('# moves (average last 10)')
plt.xlabel('episode')
plt.title(f'Moves on {track} Track with {crash_behavior} (sarsa)')
plt.show()
