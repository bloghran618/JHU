import numpy as np
from random import random, randint
from bresenham import bresenham
import yaml
import sys

from utils import *

class Board:
    def __init__(self, track_name, crash_type, output_file, verbose=True):
        # output settings
        self.verbose = verbose
        self.output_file = output_file
        
        # initialize values
        self.y = 0
        self.x = 0
        self.x_speed = 0
        self.y_speed = 0
        self.crash_type = crash_type

        # load the board into a list of lists
        self.track_name = track_name
        self.start_locs = []
        self.finish_locs = []
        self.board = self.load_board()

        # initialize x, y location to starting line and print board
        self.send_to_start()
        self.print_board()

        # set the reward for finishing
        self.finish_reward = 100


    def load_board(self):
        """
        load the board as a list of lists

        :return: the board
        """
        track_file_name = f'./tracks/{self.track_name}.txt'

        # open the track file and read in the board line by line
        track_file = open(track_file_name, 'r')
        for line_no, line in enumerate(track_file):

            # dimension the board by the size values in the track file
            if line_no == 0:
                y_dim, x_dim = line.split(',')
                board = np.empty(shape=(int(y_dim), int(x_dim)), dtype='object')
            # populate the board list of lists with board values
            else:
                for char_no, char in enumerate(line):
                    # exclude endline characters
                    if char != '\n':
                        board[line_no-1][char_no] = char
                    # track the locations of the start and finish spaces
                    if char == 'S':
                        self.start_locs.append((line_no-1, char_no))
                    if char == 'F':
                        self.finish_locs.append((line_no - 1, char_no))
        return board


    def send_to_start(self):
        """
        Send the racecar to the start line
        """
        start_loc_index = randint(0, len(self.start_locs) - 1)
        self.y = self.start_locs[start_loc_index][0]
        self.x = self.start_locs[start_loc_index][1]
        self.x_speed = 0
        self.y_speed = 0
        write_board_output(self.output_file, self.verbose, f'starting at (x={self.x}, y={self.y})')


    def stop_at_wall(self, stop_loc):
        """
        Stop the racecar at the wall it crashed into

        :param stop_loc: the last valid location of the racecar on the board
        """
        self.x_speed = 0
        self.y_speed = 0
        self.x = stop_loc[0]
        self.y = stop_loc[1]


    def accelerate(self, x_acc, y_acc):
        """
        increment the speed values by provided acceleration values

        :param x_acc: the acceleration in the x direction
        :param y_acc: the acceleration in the y direction
        """

        # give an 80% chance of success to an acceleration attempt
        if random() <= 0.8:
            # only increment the speed if the result will be in +/- 5
            if abs(self.x_speed + x_acc) <= 5:
                self.x_speed += x_acc
            if abs(self.y_speed + y_acc) <= 5:
                self.y_speed += y_acc
        else:
            write_board_output(self.output_file, self.verbose, 'the acceleration attempt failed')


    def move(self):
        """
        execute a movement maneuver
        """

        # compute the destination if the move is valid
        dest_x = self.x + self.x_speed
        dest_y = self.y + self.y_speed

        # get all the points that the car will pass through
        pass_points = list(bresenham(self.x, self.y, dest_x, dest_y))
        write_board_output(self.output_file, self.verbose, f'this maneuver will pass through: {pass_points}')

        # initialize crash and finish booleans to false
        crash = False
        finish = False

        # check each point the car passes through
        for point in pass_points:
            write_board_output(self.output_file, self.verbose, f'the board at (x={point[0]}, y={point[1]}) is {self.board[point[1]][point[0]]}')

            # if the racecar finished, stop the car on the finish line
            if self.board[point[1]][point[0]] == 'F':
                finish = True
                last_valid = point
                break

            # handle if the racecar crashed
            elif self.board[point[1]][point[0]] == '#':
                crash = True
                break
            last_valid = point

        # handle if the racecar finished
        if finish:
            write_board_output(self.output_file, self.verbose, 'hey! we finished!')
            self.stop_at_wall(last_valid)
        # if the racecar crashed, send the car back to the starting line
        elif crash and self.crash_type == 'respawn':
            write_board_output(self.output_file, self.verbose, f'we crashed, respawn at starting line')
            self.send_to_start()
        # if the racecar crashed, stop the car at the wall it crashed into
        elif crash and self.crash_type == 'bump':
            write_board_output(self.output_file, self.verbose, f'we crashed, stop at the wall')
            self.stop_at_wall(last_valid)
        # move racecar to destination if the racecar did not crash or finish
        else:
            write_board_output(self.output_file, self.verbose, f'we did not crash, execute maneuver')
            self.x += self.x_speed
            self.y += self.y_speed


    def print_state(self):
        """
        print the state including the current racecar location, speed and the board
        """
        write_board_output(self.output_file, self.verbose, f'location: (x={self.x}, y={self.y})')
        write_board_output(self.output_file, self.verbose, f'speed: x={self.x_speed}; y={self.y_speed}')
        write_board_output(self.output_file, self.verbose, f'the reward at this location is {self.get_reward()}')
        self.print_board()
        write_board_output(self.output_file, self.verbose, '')


    def get_state_array(self):
        """
        convert the state to an array

        :return: [x_loc, y_loc, x_speed, y_speed]
        """
        return [self.x, self.y, self.x_speed, self.y_speed]


    def take_action(self, x_acc, y_acc):
        """
        attempt to accelerate/move and then show the state of the board

        :param x_acc: the acceleration in the x direction
        :param y_acc: the acceleration in the y direction
        """
        self.accelerate(x_acc, y_acc)
        # self.print_state()
        self.move()
        self.print_state()


    def get_action_result(self, start_x, start_y, speed_x, speed_y):
        """
        get the result of taking action with starting position and speed

        :param start_x: the starting x location
        :param start_y: the starting y location
        :param speed_x: the starting x speed
        :param speed_y: teh starting y speed
        :return:
        """
        self.x = start_x
        self.y = start_y
        self.x_speed = speed_x
        self.y_speed = speed_y

        self.move()

        return self.get_state_array()


    def get_reward(self):
        """
        get the cost of the current board location

        :return: the location cost
        """

        # finish has a cost of - the board reward, while everything else has a cost of 1
        if self.board[self.y][self.x] == 'F':
            return self.finish_reward
        else:
            return -1


    def get_location_reward(self, x, y):
        """
        get the reward of a given board location

        :param x: the x location on the board
        :param y: the y location on the board
        :return: the reward at the given location
        """

        # finish has a cost of - the board reward, while everything else has a cost of 1
        if self.board[y][x] == 'F':
            return self.finish_reward
        else:
            return -1


    def set_verbose(self, new_val):
        """
        set verbosity

        :param new_val: the new verbosity level
        """
        self.verbose = new_val


    def print_board(self):
        """
        output the list of lists board into human readable format
        """
        for row_num, row in enumerate(self.board):
            for col_num, col in enumerate(row):

                # check if this is the location the racecar is at, and if so show '@'
                if row_num == self.y and col_num == self.x:
                    write_board_output_no_newline(self.output_file, self.verbose, '@')
                # print the value of the board
                else:
                    write_board_output_no_newline(self.output_file, self.verbose, col)
            write_board_output(self.output_file, self.verbose, '')


if __name__ == '__main__':

    # board parameters
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    track = config['track']
    crash_behavior = config['crash_behavior']
    outputfile = f'output/self-play-{track}-track-{crash_behavior}.output.txt'
    clear_file_output(outputfile)
    board = Board(track, crash_behavior, outputfile, verbose=True)

    # define the actions that the racecar can take (x and y acceleration components)
    decisions = {
        1: [-1, 1],
        2: [0, 1],
        3: [1, 1],
        4: [-1, 0],
        5: [0, 0],
        6: [1, 0],
        7: [-1, -1],
        8: [0, -1],
        9: [1, -1],
    }

    moves = 0
    while board.get_reward() < 0:

        for action_choice, action in decisions.items():
            write_output(outputfile, f'choice: {action_choice} accelerates x {action[0]} and y {action[1]}')
        action_choice = input('choose your action: ')

        if action_choice not in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            raise RuntimeError('Action is invalid, you lose')

        action = decisions[int(action_choice)]
        board.take_action(action[0], action[1])
        moves += 1

    write_output(outputfile, f'you took {moves} moves')
    sys.exit()
