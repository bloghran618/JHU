# this class represents one cell of the DTM model
class Rule:
    def __init__(self, q0, read, q1, write, write_to, s):
        self.init_state = q0
        self.read = read
        self.new_state = q1
        self.write = write
        self.write_to = write_to  # integer, defines which tape to write to (0, 1 are input tapes, 2 is output tape)
        self.move_head = s

        # make sure the move head is either 1 or -1
        if self.move_head != 1 and self.move_head != -1:
            raise TypeError("Move head <" + str(self.s) + "> is not 1 or -1")

    def __str__(self):
        return("q0=" + self.init_state + ", read=" + self.read + ", qnew=" + self.new_state +
               ", write=" + self.write + ", write_to=" + str(self.write_to) + ", s=" + str(self.move_head))


# this class represents one row of the DTM model
class TransitionTableRow:
    def __init__(self, q, in_rules):
        self.initial_state = q
        self.rules = {}

        # check that each rule's initial state matches for the row
        for rule in in_rules:
            if rule.init_state != self.initial_state:
                raise TypeError("Rule initial state <" + str(rule.init_state) +
                                "> does not match Row initial state <" + str(self.initial_state) + ">")
            else:
                self.rules[rule.read] = rule

    def __str__(self):
        string = "state=" + self.initial_state
        for key in self.rules:
            string += ("\nread=" + self.rules[key].read + ", qnew=" + self.rules[key].new_state +
                       ", write=" + self.rules[key].write + ", write_to=" + str(self.rules[key].write_to) +
                       ", s=" + str(self.rules[key].move_head))
        return string

    def get_rules(self):
        return self.rules


# this class represents the DTM model
class TransitionTable:
    def __init__(self, rows):
        self.state_functions = {}

        # get the read_vals of the first row to check against the other rows
        base_read_vals = []
        for key in rows[0].get_rules():
            base_read_vals.append(rows[0].get_rules()[key].read)

        # check that all row read_vals match to have a complete table
        for row in rows:
            row_read_vals = []
            for key in row.get_rules():
                row_read_vals.append(row.get_rules()[key].read)
            if row_read_vals != base_read_vals:
                raise TypeError("Row read_vals do not match")
            else:
                self.state_functions[row.initial_state] = row

    def __str__(self):
        string = "\nTransition Table: \n"
        for key in self.state_functions:
            string += (str(self.state_functions[key]) + "\n")

        return string

    # get all of the possible state combinations
    def get_states(self):
        states = []
        for key in self.state_functions:
            states.append(key)
        return states


# this class represents the entire turing machine
class TuringMachine:
    def __init__(self, Gamma, Q, delta, Sigma, beta, initial_state):
        self.alphabet = Gamma
        self.states = Q
        self.transition_function = delta
        self.blank = beta
        self.alphabet.append(beta)
        self.state = initial_state
        self.tape_index = 0

        # represent the tapes as a list of dictionaries
        self.tapes = []
        for tape in Sigma:
            current_tape = {}
            for letter_index, letter in enumerate(tape):
                current_tape[letter_index] = letter
            self.tapes.append(current_tape)

        # check that the states match
        if self.states != self.transition_function.get_states():
            raise TypeError("Turing machine states <" + str(self.states) + "> does not equal " +
                            "Transition table states <" + str(self.transition_function.get_states()) + ">")

    # convert the tape list of dictionaries to readable string
    def tapes_string(self):
        string = ""

        # get and sort the indexes of the tapes
        keys = []
        for tape in self.tapes:
            for key in tape:
                if key not in keys:
                    keys.append(key)
        sorted_keys = sorted(keys)

        # write tape values for each tape and maintain alignment
        string_input_1 = ""
        string_input_2 = ""
        string_output_1 = ""
        indexes = ""
        for key in sorted_keys:
            indexes += str(int(key) % 10)
            try:
                string_input_1 += self.tapes[0][key]
            except KeyError:
                string_input_1 += "#"
            try:
                string_input_2 += self.tapes[1][key]
            except KeyError:
                string_input_2 += "#"
            try:
                string_output_1 += self.tapes[2][key]
            except KeyError:
                string_output_1 += "#"

        string += "Aligned Index % 10:       " + indexes + "\n"
        string += "Tape input_1 looks like:  " + string_input_1 + "\n"
        string += "Tape input_2 looks like:  " + string_input_2 + "\n"
        string += "Tape output_1 looks like: " + string_output_1 + "\n"

        return string.strip()

    # convert a single tape to a string (useful for the return of the Turing Machine)
    def tape_string(self, tape):
        string = ""
        keys = []

        # get the index of each letter on the tape
        for key in tape:
            keys.append(key)

        # sort the indicies
        sorted_keys = sorted(keys)

        # write each letter to the string in order
        for key in sorted_keys:
            string += tape[key]

        string = string.strip("#")
        return string

    def run(self):
        while True:
            # write some parameters to output
            write_to_output("\nOperating Turing Machine cycle:")
            write_to_output("The current state is: " + self.state)
            write_to_output("The current index is: " + str(self.tape_index))
            write_to_output(self.tapes_string())

            # read the value at the current tape index for the two tapes
            try:
                read0 = self.tapes[0][self.tape_index]
            except KeyError:
                read0 = self.blank
            try:
                read1 = self.tapes[1][self.tape_index]
            except KeyError:
                read1 = self.blank
            read = read0 + read1
            write_to_output("read <" + read + "> at tape index " + str(self.tape_index))

            # get the new state, what to write to the tape, and which way to move the read head
            new_state = self.transition_function.state_functions[self.state].rules[read].new_state
            write = self.transition_function.state_functions[self.state].rules[read].write
            write_to = self.transition_function.state_functions[self.state].rules[read].write_to
            s = self.transition_function.state_functions[self.state].rules[read].move_head
            if s == 1:
                right_or_left = "right"
            else:
                right_or_left = "left"
            write_to_output("Change state to <" + new_state + ">, write <" + write +
                            "> on tape <" + str(write_to) + "> and move head " + right_or_left)

            # change state, write value, and move head
            self.state = new_state
            self.tapes[write_to][self.tape_index] = write
            self.tape_index += s

            # check if we are ready to return
            if self.state == "qn" :
                raise RuntimeError("Turing Machine reached state qn, this may be because the value on the small "
                                   "tape is larger than the value on the big tape")
            elif self.state == "qy":
                return self.tape_string(self.tapes[2])


# clear the contents of the output file
def clear_output_file():
    with open('turingMachineSub.txt', 'a') as output_file:
        output_file.seek(0)
        output_file.truncate()
        output_file.close()


# write a single line to the output
def write_to_output(string):
    with open('turingMachineSub.txt', 'a') as output_file:
        output_file.write(string + '\n')
        output_file.close()


# determine whether to write the output to the command line or to the output file (happens at the end of processing)
def dump_output():

    # check if the file is less than 30 lines
    length_of_file = len(open('turingMachineSub.txt').readlines())
    if length_of_file < 30:

        # if so, write the file to the console
        with open('turingMachineSub.txt', 'r') as output_file:
            print(output_file.read())
    else:
        print("task complete, see results in turingMachineSub.txt")


# read the values for the tapes from the given input file
def read_input():
    input_nums = []
    with open('turingMachineInput.txt') as input_file:
        for line in input_file:
            input_nums.append(line.split('=')[-1].strip())
    return input_nums


# convert a binary string to decimal number
def binary_to_number(binary_string, blank):
    binary_string = binary_string.strip(blank)
    val = 0
    for index, char in enumerate(reversed(binary_string)):
        if char == "1":
            val += 2 ** index
    return val


if __name__ == '__main__':
    clear_output_file()

    # initializing the alphabet and set of states for the turing machine
    alphabet = ['0', '1']
    blank_symbol = "#"
    states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7']

    # set the values of the input tapes
    input_numbers = read_input()
    tape_big_val = input_numbers[0]
    tape_small_val = input_numbers[1]
    tapes = [tape_big_val, tape_small_val, ""]

    # display the input numbers to operate on
    write_to_output("The larger number to subtract from is: " + tape_big_val + " ("
                    + str(binary_to_number(tape_big_val, '#')) + ")")
    write_to_output("The smaller number to subtract is: " + tape_small_val + " ("
                    + str(binary_to_number(tape_small_val, '#')) + ")")

    # # initializing each rule for the table
    ruleq0_00 = Rule('q0', '00', 'q0', '0', 1, 1)
    ruleq0_01 = Rule('q0', '01', 'q0', '1', 1, 1)
    ruleq0_10 = Rule('q0', '10', 'q0', '0', 1, 1)
    ruleq0_11 = Rule('q0', '11', 'q0', '1', 1, 1)
    ruleq0_b0 = Rule('q0', '#0', 'qn', '#', 1, 1)
    ruleq0_0b = Rule('q0', '0#', 'q1', '#', 1, -1)
    ruleq0_b1 = Rule('q0', '#1', 'qn', '#', 1, 1)
    ruleq0_1b = Rule('q0', '1#', 'q1', '#', 1, -1)
    ruleq0_bb = Rule('q0', '##', 'q6', '#', 2, -1)

    ruleq1_00 = Rule('q1', '00', 'q2', '#', 1, 1)
    ruleq1_01 = Rule('q1', '01', 'q3', '#', 1, 1)
    ruleq1_10 = Rule('q1', '10', 'q2', '#', 1, 1)
    ruleq1_11 = Rule('q1', '11', 'q3', '#', 1, 1)
    ruleq1_b0 = Rule('q1', '#0', 'qn', '#', 1, 1)
    ruleq1_0b = Rule('q1', '0#', 'q5', '#', 1, 1)
    ruleq1_b1 = Rule('q1', '#1', 'qn', '#', 1, 1)
    ruleq1_1b = Rule('q1', '1#', 'q5', '#', 1, 1)
    ruleq1_bb = Rule('q1', '##', 'q5', '#', 1, 1)

    ruleq2_00 = Rule('q2', '00', 'qn', '#', 2, 1)
    ruleq2_01 = Rule('q2', '01', 'qn', '#', 2, 1)
    ruleq2_10 = Rule('q2', '10', 'qn', '#', 2, 1)
    ruleq2_11 = Rule('q2', '11', 'qn', '#', 2, 1)
    ruleq2_b0 = Rule('q2', '#0', 'qn', '#', 2, 1)
    ruleq2_0b = Rule('q2', '0#', 'q4', '0', 1, -1)
    ruleq2_b1 = Rule('q2', '#1', 'qn', '#', 2, 1)
    ruleq2_1b = Rule('q2', '1#', 'q4', '0', 1, -1)
    ruleq2_bb = Rule('q2', '##', 'qn', '#', 2, 1)

    ruleq3_00 = Rule('q3', '00', 'qn', '#', 2, 1)
    ruleq3_01 = Rule('q3', '01', 'qn', '#', 2, 1)
    ruleq3_10 = Rule('q3', '10', 'qn', '#', 2, 1)
    ruleq3_11 = Rule('q3', '11', 'qn', '#', 2, 1)
    ruleq3_b0 = Rule('q3', '#0', 'qn', '#', 2, 1)
    ruleq3_0b = Rule('q3', '0#', 'q4', '1', 1, -1)
    ruleq3_b1 = Rule('q3', '#1', 'qn', '#', 2, 1)
    ruleq3_1b = Rule('q3', '1#', 'q4', '1', 1, -1)
    ruleq3_bb = Rule('q3', '##', 'qn', '#', 2, 1)

    ruleq4_00 = Rule('q4', '00', 'qn', '#', 2, 1)
    ruleq4_01 = Rule('q4', '01', 'qn', '#', 2, 1)
    ruleq4_10 = Rule('q4', '10', 'qn', '#', 2, 1)
    ruleq4_11 = Rule('q4', '11', 'qn', '#', 2, 1)
    ruleq4_b0 = Rule('q4', '#0', 'qn', '#', 2, 1)
    ruleq4_0b = Rule('q4', '0#', 'q1', '#', 1, -1)
    ruleq4_b1 = Rule('q4', '#1', 'qn', '#', 2, 1)
    ruleq4_1b = Rule('q4', '1#', 'q1', '#', 1, -1)
    ruleq4_bb = Rule('q4', '##', 'q0', '#', 1, 1)

    ruleq5_00 = Rule('q5', '00', 'q0', '0', 1, 1)
    ruleq5_01 = Rule('q5', '01', 'q0', '1', 1, 1)
    ruleq5_10 = Rule('q5', '10', 'q0', '0', 1, 1)
    ruleq5_11 = Rule('q5', '11', 'q0', '1', 1, 1)
    ruleq5_b0 = Rule('q5', '#0', 'qn', '#', 1, 1)
    ruleq5_0b = Rule('q5', '0#', 'q5', '#', 1, 1)
    ruleq5_b1 = Rule('q5', '#1', 'qn', '#', 1, 1)
    ruleq5_1b = Rule('q5', '1#', 'q5', '#', 1, 1)
    ruleq5_bb = Rule('q5', '##', 'qn', '#', 1, 1)

    ruleq6_00 = Rule('q6', '00', 'q6', '0', 2, -1)
    ruleq6_01 = Rule('q6', '01', 'q7', '1', 2, -1)
    ruleq6_10 = Rule('q6', '10', 'q6', '1', 2, -1)
    ruleq6_11 = Rule('q6', '11', 'q6', '0', 2, -1)
    ruleq6_b0 = Rule('q6', '#0', 'qn', '#', 2, -1)
    ruleq6_0b = Rule('q6', '0#', 'q6', '0', 2, -1)
    ruleq6_b1 = Rule('q6', '#1', 'qn', '#', 2, -1)
    ruleq6_1b = Rule('q6', '1#', 'q6', '1', 2, -1)
    ruleq6_bb = Rule('q6', '##', 'qy', '#', 2, 1)

    ruleq7_00 = Rule('q7', '00', 'q7', '1', 2, -1)
    ruleq7_01 = Rule('q7', '01', 'q7', '0', 2, -1)
    ruleq7_10 = Rule('q7', '10', 'q6', '0', 2, -1)
    ruleq7_11 = Rule('q7', '11', 'q7', '1', 2, -1)
    ruleq7_b0 = Rule('q7', '#0', 'q6', '1', 2, -1)
    ruleq7_0b = Rule('q7', '0#', 'q7', '1', 2, -1)
    ruleq7_b1 = Rule('q7', '#1', 'qn', '#', 2, -1)
    ruleq7_1b = Rule('q7', '1#', 'q6', '0', 2, -1)
    ruleq7_bb = Rule('q7', '##', 'qn', '#', 2, -1)

    # # initializing each row of the turing table
    q0 = TransitionTableRow('q0', [ruleq0_00, ruleq0_01, ruleq0_10, ruleq0_11, ruleq0_b0, ruleq0_0b, ruleq0_b1,
                                   ruleq0_1b, ruleq0_bb])
    q1 = TransitionTableRow('q1', [ruleq1_00, ruleq1_01, ruleq1_10, ruleq1_11, ruleq1_b0, ruleq1_0b, ruleq1_b1,
                                   ruleq1_1b, ruleq1_bb])
    q2 = TransitionTableRow('q2', [ruleq2_00, ruleq2_01, ruleq2_10, ruleq2_11, ruleq2_b0, ruleq2_0b, ruleq2_b1,
                                   ruleq2_1b, ruleq2_bb])
    q3 = TransitionTableRow('q3', [ruleq3_00, ruleq3_01, ruleq3_10, ruleq3_11, ruleq3_b0, ruleq3_0b, ruleq3_b1,
                                   ruleq3_1b, ruleq3_bb])
    q4 = TransitionTableRow('q4', [ruleq4_00, ruleq4_01, ruleq4_10, ruleq4_11, ruleq4_b0, ruleq4_0b, ruleq4_b1,
                                   ruleq4_1b, ruleq4_bb])
    q5 = TransitionTableRow('q5', [ruleq5_00, ruleq5_01, ruleq5_10, ruleq5_11, ruleq5_b0, ruleq5_0b, ruleq5_b1,
                                   ruleq5_1b, ruleq5_bb])
    q6 = TransitionTableRow('q6', [ruleq6_00, ruleq6_01, ruleq6_10, ruleq6_11, ruleq6_b0, ruleq6_0b, ruleq6_b1,
                                   ruleq6_1b, ruleq6_bb])
    q7 = TransitionTableRow('q7', [ruleq7_00, ruleq7_01, ruleq7_10, ruleq7_11, ruleq7_b0, ruleq7_0b, ruleq7_b1,
                                   ruleq7_1b, ruleq7_bb])

    # initializing the transition table
    table = TransitionTable([q0, q1, q2, q3, q4, q5, q6, q7])
    write_to_output(str(table))

    # initializing the turing machine
    TM = TuringMachine(alphabet, states, table, tapes, blank_symbol, states[0])

    try:
        result = TM.run()

        # write the result of the turing machine
        write_to_output("\nTuring machine successfully ran. Result is: " + result)
        write_to_output("\nOr if you prefer, " + str(binary_to_number(tape_big_val, blank_symbol)) + " - " +
                        str(binary_to_number(tape_small_val, blank_symbol)) + " = " +
                        str(binary_to_number(result, blank_symbol)))
    except RuntimeError:
        write_to_output("Turing machine run failed, is the value for the small tape larger than the value for " +
                        "the big tape?")

    dump_output()
