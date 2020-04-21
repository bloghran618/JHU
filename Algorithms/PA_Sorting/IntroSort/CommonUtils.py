import random


def read_input(file_name):
    vals = []
    with open(file_name) as file:
        lines = file.readlines()

        # allow the user to create array of random vals
        if lines[0].strip().lower() == "random values":
            vals = create_random_vals(int(lines[1]), int(lines[2]))

        # allow the user to create an array of vals in backwards order
        elif lines[0].strip().lower() == "backwards values":
            vals = create_backwards_vals(int(lines[1]))

        # or read the vals directly from the file
        else:
            for line in lines:
                try:
                    val = int(line.strip())
                    vals.append(val)
                except:
                    pass

        file.close()

    return vals


def create_random_vals(num_vals, max_val):
    # initialize points and iterator
    vals = []
    i = 0

    # create a random point in the specified range
    while i < num_vals:
        vals.append(random.randint(0, max_val))
        i += 1

    return vals


def create_backwards_vals(num_vals):
    vals = []

    # create sequential points in reverse sorted order
    for num in range(num_vals):
        vals.append(num_vals - num)

    return vals


def clear_output_file(file_name):
    with open(file_name, 'a') as output_file:
        output_file.seek(0)
        output_file.truncate()
        output_file.close()


def write_to_output(file_name, string):
    with open(file_name, 'a') as output_file:
        string = str(string)
        output_file.write(string + '\n')
        output_file.close()


def dump_output(file_name):
    # check if the file is less than 50 lines
    length_of_file = len(open(file_name).readlines())
    if length_of_file < 50:

        # if so, write the file to the console
        with open(file_name, 'r') as output_file:
            print(output_file.read())
    else:
        print("task complete, see results in " + file_name)


# swap two values in the array by index
def swap(array, index1, index2):
    val1 = array[index1]
    val2 = array[index2]
    array[index1] = val2
    array[index2] = val1
    return array


# place a subarray into an array at a specified index (useful for putting heapsorted valued back into main array)
def place_subarray(subarray, array, index):
    if (len(subarray) + index) > len(array):
        raise IndexError("Subarray of length " + str(len(subarray)) + "placed at index " + str(index) +
                         "will exceed last index of array of length " + str(len(array)))

    for val in subarray:
        array[index] = val
        index += 1

    return array
