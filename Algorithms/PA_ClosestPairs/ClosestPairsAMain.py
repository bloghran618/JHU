import random
import math
import timeit


def clear_output_file():
    with open('closestPairsAOutput.txt', 'a') as output_file:
        output_file.seek(0)
        output_file.truncate()
        output_file.close()


def write_to_output(string):
    with open('closestPairsAOutput.txt', 'a') as output_file:
        output_file.write(string + '\n')
        output_file.close()


def dump_output():

    # check if the file is less than 30 lines
    length_of_file = len(open('closestPairsAOutput.txt').readlines( ))
    if length_of_file < 30:

        # if so, write the file to the console
        with open('closestPairsAOutput.txt', 'r') as output_file:
            print(output_file.read())
    else:
        print("task complete, see results in closestPairsAOutput.txt")


def write_points_to_output(points):
    write_to_output("There are " + str(len(points)) + " points in the set: ")
    for point in points:
        write_to_output(str(point))
    write_to_output("")


# read the points from an input file in the format:
# 1, 2
# 2, 4
# 5, 2
# ...
def read_points():
    points = []
    with open("closestPairsInput.txt") as file:
        lines = file.readlines()

        # allow the user to create array of random points
        if lines[0].strip() == "Randomize Points":
            points = create_random_point_list(int(lines[1]), int(lines[2]), int(lines[3]))

        # or read the points directly from the file
        else:
            for line in lines:
                x = int(line.split(",")[0].strip())
                y = int(line.split(",")[1].strip())
                points.append([x, y])

        file.close()

    return points


def create_random_point_list(num_points, max_x, max_y):
    # initialize points and iterator
    points = []
    i = 0

    # create the number of points specified in the specified range
    while i < num_points:
        # create a point in range
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        point = [x, y]

        # add the point if it does not already exist
        if not (point in points):
            # add it to the list of points
            points.append(point)
            i += 1

    return points


def calculate_euclidean_distance(point_a, point_b):
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)


# assumes points are supplied as 2D array as follows:
#    [[1, 5],
#     [2, 4],
#     [3, 3],
#     ...
#     ]
def closest_distance_in_set(points):
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

                    write_to_output("New closest is dist " + str(dist) + " between " + str(point_a) + " and "
                                    + str(point_b))

                    min_dist = dist
                    result_point_a = point_a
                    result_point_b = point_b

    return("\nThe minimum distance is " + str(min_dist) +
            " between " + str(result_point_a) + " and " + str(result_point_b))


if __name__ == '__main__':

    clear_output_file()

    # read points from file
    newPoints = read_points()

    # get the closest distance in the set
    write_points_to_output(newPoints)
    write_to_output(closest_distance_in_set(newPoints))

    # use python timeit library to compute algorithmic solve time
    num_tests = 10
    write_to_output(closest_distance_in_set(newPoints))
    write_to_output("The amount of time for Closest Pairs for " + str(len(newPoints)) + " points is: " +
                    str(timeit.timeit("closest_distance_in_set(newPoints)",
                        setup="from __main__ import closest_distance_in_set",
                        globals=globals(),
                        number=num_tests)
          /num_tests) + "s")

    # write the output to the console if it is less than 30 lines
    dump_output()
