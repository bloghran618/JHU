from KnownSignal import KnownSignal
from PossibleSolution import PossibleSolution

# specify the input and output file
input_file = 'SignalInput.txt'
output_file = 'UnweaveOutput.txt'


def clear_output_file():
    with open(output_file, 'a') as file:
        file.seek(0)
        file.truncate()
        file.close()


def write_to_output(string):
    with open(output_file, 'a') as file:
        string = str(string)
        file.write(string + '\n')
        file.close()


def dump_output(output_file):
    # check if the file is less than 50 lines
    length_of_file = len(open(output_file).readlines())
    if length_of_file < 50:

        # if so, write the file to the console
        with open(output_file, 'r') as output_file:
            print(output_file.read())
    else:
        print("task complete, see results in " + output_file)


# read a single line from the input file
def read_line(line_num):
    with open(input_file) as file:
        lines = file.readlines()
        file.close()
        return lines[line_num].strip()


# get the signal from the input file as a string
def read_signal():
    return read_line(0).strip()


def read_x():
    signal_x = read_line(1).strip()
    return KnownSignal(signal_x)


def read_y():
    signal_y = read_line(2).strip()
    return KnownSignal(signal_y)


# create a set of possible solutions for the next index of s based on the last set of solutions
def permute_possible_solutions(old_possible_solutions, x, y):
    new_possible_solutions = []

    # if possible solutions is empty try the current index of x and y
    if not old_possible_solutions:

        # one possible solution is if the next char is x
        signal = x.get_val_at_current_index()
        breakdown = ['x']
        final_x_index = x.add_val_and_index(1, x.get_index())
        final_y_index = y.get_index()
        possible_solution = PossibleSolution(signal, breakdown, final_x_index, final_y_index)
        new_possible_solutions.append(possible_solution)

        # another possible solution is if the next char is y
        signal = y.get_val_at_current_index()
        breakdown = ['y']
        final_x_index = x.get_index()
        final_y_index = y.add_val_and_index(1, y.get_index())
        possible_solution = PossibleSolution(signal, breakdown, final_x_index, final_y_index)
        new_possible_solutions.append(possible_solution)

    # if there are already possible solutions permute off those
    else:
        for solution in old_possible_solutions:

            # one possible solution is if the next val is from x
            old_signal = solution.get_signal()
            new_bit = x.get_val_at_index(solution.get_fin_x_index())
            new_signal = old_signal + new_bit
            breakdown = solution.get_signal_breakdown() + ['x']
            final_x_index = x.add_val_and_index(1, solution.get_fin_x_index())
            final_y_index = solution.get_fin_y_index()
            possible_solution = PossibleSolution(new_signal, breakdown, final_x_index, final_y_index)
            new_possible_solutions.append(possible_solution)

            # one other possible solution is if the next val is from y
            old_signal = solution.get_signal()
            new_bit = y.get_val_at_index(solution.get_fin_y_index())
            new_signal = old_signal + new_bit
            breakdown = solution.get_signal_breakdown() + ['y']
            final_x_index = solution.get_fin_x_index()
            final_y_index = y.add_val_and_index(1, solution.get_fin_y_index())
            possible_solution = PossibleSolution(new_signal, breakdown, final_x_index, final_y_index)
            new_possible_solutions.append(possible_solution)

    return new_possible_solutions


# remove solutions that are not correct
def pop_incorrect_solutions(candidate_solutions, match_string):
    possible_solutions = []

    # check each solution to see if their signal matches
    for solution in candidate_solutions:
        if solution.get_signal() == match_string:
            possible_solutions.append(solution)

    return possible_solutions


# any solution with the same final_x_index and final_y_index are effectively duplicates, remove them
def pop_duplicates(poss_solutions):
    recorded_final_indexes = {}
    possible_solutions = []

    for solution in poss_solutions:
        final_x = solution.get_fin_x_index()
        final_y = solution.get_fin_y_index()

        # hash is the dictionary entry for the final x index and final y index pair
        hash = str(final_x) + '-' + str(final_y)

        if not recorded_final_indexes.get(hash):
            recorded_final_indexes[hash] = True

            possible_solutions.append(solution)

    return possible_solutions


# check if the signal s can be unwoven into x and y
def unweave(s, x, y):

    # initialize some helpful variables
    s_index = 0
    unassigned = ""
    poss_solutions = []
    unwoven = []
    counter = 0

    # check the signal is long enough for at least one full match of x and y
    if len(s) < (x.get_signal_length() + y.get_signal_length()):
        write_to_output("Signal s is not big enough to find a full match of x and y")
        return False

    # iterate through each index in s
    while s_index < len(s):
        write_to_output("\nLooking at index " + str(s_index) + " in s:")

        unassigned += s[s_index]

        write_to_output("The unassigned values from s are: " + unassigned)

        # create a set of solutions for the next index in s
        poss_solutions = permute_possible_solutions(poss_solutions, x, y)
        write_to_output("\nThe " + str(len(poss_solutions)) + " permuted solutions are:")
        for solution in poss_solutions:
            write_to_output(solution)

            # increment counter for each of the solutions we have to check
            counter += 1

        # check each of the solutions to see if they match the signal
        poss_solutions = pop_incorrect_solutions(poss_solutions, unassigned)
        write_to_output("\nThe " + str(len(poss_solutions)) + " solutions that match s are:")
        for solution in poss_solutions:
            write_to_output(solution)

            # increment counter for each of the solutions we have to check
            counter += 1

        # remove duplicate solutions
        poss_solutions = pop_duplicates(poss_solutions)
        write_to_output("\nThe " + str(len(poss_solutions)) + " non-duplicate solutions are:")
        for solution in poss_solutions:
            write_to_output(solution)

            # increment counter for each of the solutions we have to check
            counter += 1

        # if there are no solutions the signal cannot be unwoven
        if len(poss_solutions) == 0:
            write_to_output("There is no possible unweaving solution")
            return False

        # if there is just one solution, add it to memory
        if len(poss_solutions) == 1:
            write_to_output("\nThere is just one solution, it must be correct")
            unassigned = ""
            unwoven = unwoven + poss_solutions[0].get_signal_breakdown()
            x.set_index(poss_solutions[0].get_fin_x_index())
            y.set_index(poss_solutions[0].get_fin_y_index())
            write_to_output("The solution through index " + str(s_index) + " is: " + str(unwoven))
            poss_solutions = []

        s_index += 1
    # end while loop, s is processed

    # if there are multiple solutions at the end of s, just grab the first one
    if poss_solutions:
        unwoven = unwoven + poss_solutions[0].get_signal_breakdown()

    # check if there were enough x's and y's in the solution to get a full match
    xs = 0
    ys = 0
    for symbol in unwoven:
        if symbol == 'x':
            xs += 1
        else:
            ys += 1
    if xs >= x.get_signal_length() and ys >= y.get_signal_length():
        write_to_output("\nSuccess, see solution below: ")
        write_to_output("The number of comparisons was: " + str(counter))
        return unwoven
    elif xs < x.get_signal_length():
        write_to_output("\nNot enough x's in solution:")
        write_to_output(unwoven)
        write_to_output("To determine a full match of x")
    elif ys < y.get_signal_length():
        write_to_output("\nNot enough y's in solution:")
        write_to_output(unwoven)
        write_to_output("To determine a full match of y")


if __name__ == '__main__':
    clear_output_file()

    # read the inputs from SignalInput.txt
    s = read_signal()
    x = read_x()
    y = read_y()

    # echo the input values to output
    write_to_output("s: " + s)
    write_to_output("x: " + x.get_signal())
    write_to_output("y: " + y.get_signal() + "\n")

    # unweave the signal s into x and y and save the solution to sol
    sol = unweave(s, x, y)

    if sol:
        write_to_output("The signal s: " + s)
        write_to_output("can be unwoven into x and y:")
        write_to_output("x: " + x.get_signal())
        write_to_output("y: " + y.get_signal())
        write_to_output("Via the following pattern: " + str(sol))

    dump_output(output_file)