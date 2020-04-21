import random
import math
import timeit
import copy

from ClosestPairsAMain import create_random_point_list, read_points


class ClosestPair:
    def __init__(self, point_a, point_b, dist):
        self.point_a = point_a
        self.point_b = point_b
        self.dist = dist

    def write_closest(self):
        write_to_output("The minimum distance is " + str(self.dist) +
                " between " + str(self.point_a) + " and " + str(self.point_b))


def clear_output_file():
    with open('closestPairsBOutput.txt', 'a') as output_file:
        output_file.seek(0)
        output_file.truncate()
        output_file.close()


def write_to_output(string):
    with open('closestPairsBOutput.txt', 'a') as output_file:
        output_file.write(string + '\n')
        output_file.close()


def dump_output():

    # check if the file is less than 30 lines
    length_of_file = len(open('closestPairsBOutput.txt').readlines( ))
    if length_of_file < 30:

        # if so, write the file to the console
        with open('closestPairsBOutput.txt', 'r') as output_file:
            print(output_file.read())
    else:
        print("task complete, see results in closestPairsBOutput.txt")


def write_points_to_output(points):
    write_to_output("There are " + str(len(points)) + " points in the set: ")
    for point in points:
        write_to_output(str(point))
    write_to_output("")


def calculate_euclidean_distance(point_a, point_b):
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)


# merge sort is O(n log(n))
def merge_sort(points, coord):
    if len(points) > 1:

        # divide array in half
        mid = len(points) // 2
        left = points[:mid]
        right = points[mid:]

        # recursively sort on both halves
        merge_sort(left, coord)
        merge_sort(right, coord)

        left_index = 0
        right_index = 0
        list_index = 0

        # translate coordinate into array position (x is position 0, y is position 1)
        if coord.lower() == 'x':
            x_or_y = 0
        else:
            x_or_y = 1

        # merge left and right
        while left_index < len(left) and right_index < len(right):
            if left[left_index][x_or_y] < right[right_index][x_or_y]:
                points[list_index] = left[left_index]
                left_index += 1
            else:
                points[list_index] = right[right_index]
                right_index += 1
            list_index += 1

        # dump any remaining items from left
        while left_index < len(left):
            points[list_index] = left[left_index]
            left_index += 1
            list_index += 1

        # dump any remaining items from right
        while right_index < len(right):
            points[list_index] = right[right_index]
            right_index += 1
            list_index += 1


def brute_closest_distance_in_set(points):
    write_to_output("Using brute force for following 2-3 points: " + str(points))

    # set the lowest distance between two points to infinity for initialization purposes
    min_dist = math.inf

    # iterate over each point in the point list
    for point_a in points:
        for point_b in points:

            # do not measure the distance if the points are the same point
            if point_a != point_b:

                # calculate the distance between the points
                dist = calculate_euclidean_distance(point_a, point_b)

                # if this is the lowest distance yet, store the point
                if dist < min_dist:
                    min_dist = dist
                    result_point_a = point_a
                    result_point_b = point_b

    closest = ClosestPair(result_point_a, result_point_b, min_dist)
    closest.write_closest()

    return closest


def closest_dist_strip(points, min_outside_dist):
    write_to_output("The minimum distance outside the strip is: " + str(min_outside_dist))

    min_dist = math.inf

    # initialize result points
    result_point_a = 0
    result_point_b = 0

    # iterate over each point in the list
    for index in range(len(points)):
        left_index = index
        right_index = index

        # check points below the current point in y (max 4 points -> O(1))
        left_index -= 1
        while left_index >= 0 and ((points[index][1] - points[left_index][1]) < min_dist):
            if calculate_euclidean_distance(points[index], points[left_index]) < min_dist:
                min_dist = calculate_euclidean_distance(points[index], points[left_index])
                result_point_a = points[index]
                result_point_b = points[left_index]
            left_index -= 1

        # check points above the current point in y (max 4 points -> O(1))
        right_index += 1
        while right_index < len(points) and ((points[right_index][1] - points[index][1]) < min_dist):
            if calculate_euclidean_distance(points[index], points[right_index]) < min_dist:
                min_dist = calculate_euclidean_distance(points[index], points[right_index])
                result_point_a = points[index]
                result_point_b = points[right_index]
            right_index += 1

    closest = ClosestPair(result_point_a, result_point_b, min_dist)
    closest.write_closest()

    return closest


def closest_distance_fast(points_x, points_y):

    write_to_output("The input points are: " + str(points_x))

    # compare each point individually if there are 2 or 3 points
    if len(points_x) <= 3:
        return brute_closest_distance_in_set(points_x)

    # get the midpoint
    mid_index = len(points_x) // 2
    mid_x = points_x[mid_index]

    # get the left and right hand side of the points sorted in x O(n)
    points_x_left = points_x[:mid_index]
    points_x_right = points_x[mid_index:]

    # get the left and right hand side of the points sorted in y O(n)
    points_y_left = []
    points_y_right = []
    for point in points_y:
        if point[0] == mid_x[0]:
            if point in points_x_left:
                points_y_left.append(point)
            else:
                points_y_right.append(point)
        elif point[0] < mid_x[0]:
            points_y_left.append(point)
        else:
            points_y_right.append(point)

    write_to_output("left half of points: " + str(points_x_left))
    write_to_output("right half of points: " + str(points_x_right))

    # recursively find the minimum on the left and the right
    min_left = closest_distance_fast(points_x_left, points_y_left)
    min_right = closest_distance_fast(points_x_right, points_y_right)

    # calculate the minimum distance of the points on the outside
    if min_left.dist < min_right.dist:
        min_outside = min_left
    else:
        min_outside = min_right

    # construct the strip in the middle
    strip_points = []
    for point in points_y:
        if abs(point[0] - mid_x[0]) < min_outside.dist:
            strip_points.append(point)

    write_to_output("The points in the strip are: " + str(strip_points))

    # get the minimum distance between points in the strip if there is more than 1 point
    if len(strip_points) > 1:
        min_strip = closest_dist_strip(strip_points, min_outside.dist)
    else:
        min_strip = ClosestPair(0, 0, math.inf)

    # return the value of the closest pair
    if min_strip.dist < min_outside.dist:
        return min_strip
    else:
        return min_outside


if __name__ == '__main__':

    clear_output_file()

    # create points list and output to file
    new_points_x = read_points()
    write_points_to_output(new_points_x)

    # create a copy of the points
    new_points_y = copy.copy(new_points_x)

    # merge sort the points in x and y
    merge_sort(new_points_x, 'x')
    merge_sort(new_points_y, 'y')

    # solve for the closest points in a more algorithmically efficient way
    closest = closest_distance_fast(new_points_x, new_points_y)
    write_to_output("\n")
    closest.write_closest()

    # # use python timeit library to compute algorithmic solve time
    num_tests = 10
    # write_to_output(closest_distance_in_set(newPoints))
    write_to_output("The amount of time for Closest Pairs Improved Algorithm for " + str(len(new_points_x)) + " points is: " +
                    str(timeit.timeit("closest_distance_fast(new_points_x, new_points_y)",
                                      setup="from __main__ import closest_distance_fast",
                                      globals=globals(),
                                      number=num_tests)
                        / num_tests) + "s")

    # write the output to the console if it is less than 30 lines
    dump_output()
