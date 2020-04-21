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
            try:
                read2 = self.tapes[2][self.tape_index]
            except KeyError:
                read2 = self.blank
            read = read0 + read1 + read2
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
    with open('turingMachineMul.txt', 'a') as output_file:
        output_file.seek(0)
        output_file.truncate()
        output_file.close()


# write a single line to the output
def write_to_output(string):
    with open('turingMachineMul.txt', 'a') as output_file:
        output_file.write(string + '\n')
        output_file.close()


# determine whether to write the output to the command line or to the output file (happens at the end of processing)
def dump_output():

    # check if the file is less than 30 lines
    length_of_file = len(open('turingMachineMul.txt').readlines())
    if length_of_file < 30:

        # if so, write the file to the console
        with open('turingMachineMul.txt', 'r') as output_file:
            print(output_file.read())
    else:
        print("task complete, see results in turingMachineMul.txt")


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
    states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13', 'q14', 'q15', 'q16']

    # set the values of the input tapes
    input_numbers = read_input()
    tape_big_val = input_numbers[0]
    tape_small_val = input_numbers[1]
    tapes = [tape_big_val, tape_small_val, ""]

    # display the input numbers to operate on
    write_to_output("The larger number to multiply with is: " + tape_big_val + " ("
                    + str(binary_to_number(tape_big_val, '#')) + ")")
    write_to_output("The smaller number to multiply is: " + tape_small_val + " ("
                    + str(binary_to_number(tape_small_val, '#')) + ")")

    # # initializing each rule for the table
    ruleq0_000 = Rule('q0', '000', 'q0', '0', 1, 1)
    ruleq0_001 = Rule('q0', '001', 'q0', '0', 1, 1)
    ruleq0_010 = Rule('q0', '010', 'q0', '1', 1, 1)
    ruleq0_011 = Rule('q0', '011', 'q0', '1', 1, 1)
    ruleq0_100 = Rule('q0', '100', 'q0', '0', 1, 1)
    ruleq0_101 = Rule('q0', '101', 'q0', '0', 1, 1)
    ruleq0_110 = Rule('q0', '110', 'q0', '1', 1, 1)
    ruleq0_111 = Rule('q0', '111', 'q0', '1', 1, 1)
    ruleq0_00b = Rule('q0', '00#', 'q0', '0', 1, 1)
    ruleq0_01b = Rule('q0', '01#', 'q0', '1', 1, 1)
    ruleq0_10b = Rule('q0', '10#', 'q0', '0', 1, 1)
    ruleq0_11b = Rule('q0', '11#', 'q0', '1', 1, 1)
    ruleq0_0b0 = Rule('q0', '0#0', 'q1', '#', 1, -1)
    ruleq0_0b1 = Rule('q0', '0#1', 'q1', '#', 1, -1)
    ruleq0_1b0 = Rule('q0', '1#0', 'q1', '#', 1, -1)
    ruleq0_1b1 = Rule('q0', '1#1', 'q1', '#', 1, -1)
    ruleq0_b00 = Rule('q0', '#00', 'qn', '#', 1, 1)
    ruleq0_b01 = Rule('q0', '#01', 'qn', '#', 1, 1)
    ruleq0_b10 = Rule('q0', '#10', 'qn', '#', 1, 1)
    ruleq0_b11 = Rule('q0', '#11', 'qn', '#', 1, 1)
    ruleq0_0bb = Rule('q0', '0##', 'q1', '#', 1, -1)
    ruleq0_1bb = Rule('q0', '1##', 'q1', '#', 1, -1)
    ruleq0_b0b = Rule('q0', '#0#', 'qn', '#', 1, 1)
    ruleq0_b1b = Rule('q0', '#1#', 'qn', '#', 1, 1)
    ruleq0_bb0 = Rule('q0', '##0', 'q11', '#', 1, -1)
    ruleq0_bb1 = Rule('q0', '##1', 'q11', '#', 1, -1)
    ruleq0_bbb = Rule('q0', '###', 'q11', '#', 1, -1)

    ruleq1_000 = Rule('q1', '000', 'q2', '#', 1, 1)
    ruleq1_001 = Rule('q1', '001', 'q2', '#', 1, 1)
    ruleq1_010 = Rule('q1', '010', 'q3', '#', 1, 1)
    ruleq1_011 = Rule('q1', '011', 'q3', '#', 1, 1)
    ruleq1_100 = Rule('q1', '100', 'q2', '#', 1, 1)
    ruleq1_101 = Rule('q1', '101', 'q2', '#', 1, 1)
    ruleq1_110 = Rule('q1', '110', 'q3', '#', 1, 1)
    ruleq1_111 = Rule('q1', '111', 'q3', '#', 1, 1)
    ruleq1_00b = Rule('q1', '00#', 'q2', '#', 1, 1)
    ruleq1_01b = Rule('q1', '01#', 'q3', '#', 1, 1)
    ruleq1_10b = Rule('q1', '10#', 'q2', '#', 1, 1)
    ruleq1_11b = Rule('q1', '11#', 'q3', '#', 1, 1)
    ruleq1_0b0 = Rule('q1', '0#0', 'q5', '#', 1, 1)
    ruleq1_0b1 = Rule('q1', '0#1', 'q5', '#', 1, 1)
    ruleq1_1b0 = Rule('q1', '1#0', 'q5', '#', 1, 1)
    ruleq1_1b1 = Rule('q1', '1#1', 'q5', '#', 1, 1)
    ruleq1_b00 = Rule('q1', '#00', 'qn', '#', 1, 1)
    ruleq1_b01 = Rule('q1', '#01', 'qn', '#', 1, 1)
    ruleq1_b10 = Rule('q1', '#10', 'qn', '#', 1, 1)
    ruleq1_b11 = Rule('q1', '#11', 'qn', '#', 1, 1)
    ruleq1_0bb = Rule('q1', '0##', 'q5', '#', 1, 1)
    ruleq1_1bb = Rule('q1', '1##', 'q5', '#', 1, 1)
    ruleq1_b0b = Rule('q1', '#0#', 'qn', '#', 1, 1)
    ruleq1_b1b = Rule('q1', '#1#', 'qn', '#', 1, 1)
    ruleq1_bb0 = Rule('q1', '##0', 'q5', '#', 1, 1)
    ruleq1_bb1 = Rule('q1', '##1', 'q5', '#', 1, 1)
    ruleq1_bbb = Rule('q1', '###', 'q5', '#', 1, 1)

    ruleq2_000 = Rule('q2', '000', 'qn', '#', 1, 1)
    ruleq2_001 = Rule('q2', '001', 'qn', '#', 1, 1)
    ruleq2_010 = Rule('q2', '010', 'qn', '#', 1, 1)
    ruleq2_011 = Rule('q2', '011', 'qn', '#', 1, 1)
    ruleq2_100 = Rule('q2', '100', 'qn', '#', 1, 1)
    ruleq2_101 = Rule('q2', '101', 'qn', '#', 1, 1)
    ruleq2_110 = Rule('q2', '110', 'qn', '#', 1, 1)
    ruleq2_111 = Rule('q2', '111', 'qn', '#', 1, 1)
    ruleq2_00b = Rule('q2', '00#', 'qn', '#', 1, 1)
    ruleq2_01b = Rule('q2', '01#', 'qn', '#', 1, 1)
    ruleq2_10b = Rule('q2', '10#', 'qn', '#', 1, 1)
    ruleq2_11b = Rule('q2', '11#', 'qn', '#', 1, 1)
    ruleq2_0b0 = Rule('q2', '0#0', 'q4', '0', 1, -1)
    ruleq2_0b1 = Rule('q2', '0#1', 'q4', '0', 1, -1)
    ruleq2_1b0 = Rule('q2', '1#0', 'q4', '0', 1, -1)
    ruleq2_1b1 = Rule('q2', '1#1', 'q4', '0', 1, -1)
    ruleq2_b00 = Rule('q2', '#00', 'qn', '#', 1, 1)
    ruleq2_b01 = Rule('q2', '#01', 'qn', '#', 1, 1)
    ruleq2_b10 = Rule('q2', '#10', 'qn', '#', 1, 1)
    ruleq2_b11 = Rule('q2', '#11', 'qn', '#', 1, 1)
    ruleq2_0bb = Rule('q2', '0##', 'q4', '0', 1, -1)
    ruleq2_1bb = Rule('q2', '1##', 'q4', '0', 1, -1)
    ruleq2_b0b = Rule('q2', '#0#', 'qn', '#', 1, 1)
    ruleq2_b1b = Rule('q2', '#1#', 'qn', '#', 1, 1)
    ruleq2_bb0 = Rule('q2', '##0', 'qn', '#', 1, 1)
    ruleq2_bb1 = Rule('q2', '##1', 'qn', '#', 1, 1)
    ruleq2_bbb = Rule('q2', '###', 'qn', '#', 1, 1)

    ruleq3_000 = Rule('q3', '000', 'qn', '#', 1, 1)
    ruleq3_001 = Rule('q3', '001', 'qn', '#', 1, 1)
    ruleq3_010 = Rule('q3', '010', 'qn', '#', 1, 1)
    ruleq3_011 = Rule('q3', '011', 'qn', '#', 1, 1)
    ruleq3_100 = Rule('q3', '100', 'qn', '#', 1, 1)
    ruleq3_101 = Rule('q3', '101', 'qn', '#', 1, 1)
    ruleq3_110 = Rule('q3', '110', 'qn', '#', 1, 1)
    ruleq3_111 = Rule('q3', '111', 'qn', '#', 1, 1)
    ruleq3_00b = Rule('q3', '00#', 'qn', '#', 1, 1)
    ruleq3_01b = Rule('q3', '01#', 'qn', '#', 1, 1)
    ruleq3_10b = Rule('q3', '10#', 'qn', '#', 1, 1)
    ruleq3_11b = Rule('q3', '11#', 'qn', '#', 1, 1)
    ruleq3_0b0 = Rule('q3', '0#0', 'q4', '1', 1, -1)
    ruleq3_0b1 = Rule('q3', '0#1', 'q4', '1', 1, -1)
    ruleq3_1b0 = Rule('q3', '1#0', 'q4', '1', 1, -1)
    ruleq3_1b1 = Rule('q3', '1#1', 'q4', '1', 1, -1)
    ruleq3_b00 = Rule('q3', '#00', 'qn', '#', 1, 1)
    ruleq3_b01 = Rule('q3', '#01', 'qn', '#', 1, 1)
    ruleq3_b10 = Rule('q3', '#10', 'qn', '#', 1, 1)
    ruleq3_b11 = Rule('q3', '#11', 'qn', '#', 1, 1)
    ruleq3_0bb = Rule('q3', '0##', 'q4', '1', 1, -1)
    ruleq3_1bb = Rule('q3', '1##', 'q4', '1', 1, -1)
    ruleq3_b0b = Rule('q3', '#0#', 'qn', '#', 1, 1)
    ruleq3_b1b = Rule('q3', '#1#', 'qn', '#', 1, 1)
    ruleq3_bb0 = Rule('q3', '##0', 'qn', '#', 1, 1)
    ruleq3_bb1 = Rule('q3', '##1', 'qn', '#', 1, 1)
    ruleq3_bbb = Rule('q3', '###', 'qn', '#', 1, 1)

    ruleq4_000 = Rule('q4', '000', 'qn', '#', 1, 1)
    ruleq4_001 = Rule('q4', '001', 'qn', '#', 1, 1)
    ruleq4_010 = Rule('q4', '010', 'qn', '#', 1, 1)
    ruleq4_011 = Rule('q4', '011', 'qn', '#', 1, 1)
    ruleq4_100 = Rule('q4', '100', 'qn', '#', 1, 1)
    ruleq4_101 = Rule('q4', '101', 'qn', '#', 1, 1)
    ruleq4_110 = Rule('q4', '110', 'qn', '#', 1, 1)
    ruleq4_111 = Rule('q4', '111', 'qn', '#', 1, 1)
    ruleq4_00b = Rule('q4', '00#', 'qn', '#', 1, 1)
    ruleq4_01b = Rule('q4', '01#', 'qn', '#', 1, 1)
    ruleq4_10b = Rule('q4', '10#', 'qn', '#', 1, 1)
    ruleq4_11b = Rule('q4', '11#', 'qn', '#', 1, 1)
    ruleq4_0b0 = Rule('q4', '0#0', 'q1', '#', 1, -1)
    ruleq4_0b1 = Rule('q4', '0#1', 'q1', '#', 1, -1)
    ruleq4_1b0 = Rule('q4', '1#0', 'q1', '#', 1, -1)
    ruleq4_1b1 = Rule('q4', '1#1', 'q1', '#', 1, -1)
    ruleq4_b00 = Rule('q4', '#00', 'qn', '#', 1, 1)
    ruleq4_b01 = Rule('q4', '#01', 'qn', '#', 1, 1)
    ruleq4_b10 = Rule('q4', '#10', 'qn', '#', 1, 1)
    ruleq4_b11 = Rule('q4', '#11', 'qn', '#', 1, 1)
    ruleq4_0bb = Rule('q4', '0##', 'q1', '#', 1, -1)
    ruleq4_1bb = Rule('q4', '1##', 'q1', '#', 1, -1)
    ruleq4_b0b = Rule('q4', '#0#', 'qn', '#', 1, 1)
    ruleq4_b1b = Rule('q4', '#1#', 'qn', '#', 1, 1)
    ruleq4_bb0 = Rule('q4', '##0', 'q0', '#', 1, 1)
    ruleq4_bb1 = Rule('q4', '##1', 'q0', '#', 1, 1)
    ruleq4_bbb = Rule('q4', '###', 'q0', '#', 1, 1)

    ruleq5_000 = Rule('q5', '000', 'q0', '0', 1, 1)
    ruleq5_001 = Rule('q5', '001', 'q0', '0', 1, 1)
    ruleq5_010 = Rule('q5', '010', 'q0', '1', 1, 1)
    ruleq5_011 = Rule('q5', '011', 'q0', '1', 1, 1)
    ruleq5_100 = Rule('q5', '100', 'q0', '0', 1, 1)
    ruleq5_101 = Rule('q5', '101', 'q0', '0', 1, 1)
    ruleq5_110 = Rule('q5', '110', 'q0', '1', 1, 1)
    ruleq5_111 = Rule('q5', '111', 'q0', '1', 1, 1)
    ruleq5_00b = Rule('q5', '00#', 'q0', '0', 1, 1)
    ruleq5_01b = Rule('q5', '01#', 'q0', '1', 1, 1)
    ruleq5_10b = Rule('q5', '10#', 'q0', '0', 1, 1)
    ruleq5_11b = Rule('q5', '11#', 'q0', '1', 1, 1)
    ruleq5_0b0 = Rule('q5', '0#0', 'q5', '#', 1, 1)
    ruleq5_0b1 = Rule('q5', '0#1', 'q5', '#', 1, 1)
    ruleq5_1b0 = Rule('q5', '1#0', 'q5', '#', 1, 1)
    ruleq5_1b1 = Rule('q5', '1#1', 'q5', '#', 1, 1)
    ruleq5_b00 = Rule('q5', '#00', 'qn', '#', 1, 1)
    ruleq5_b01 = Rule('q5', '#01', 'qn', '#', 1, 1)
    ruleq5_b10 = Rule('q5', '#10', 'qn', '#', 1, 1)
    ruleq5_b11 = Rule('q5', '#11', 'qn', '#', 1, 1)
    ruleq5_0bb = Rule('q5', '0##', 'q5', '#', 1, 1)
    ruleq5_1bb = Rule('q5', '1##', 'q5', '#', 1, 1)
    ruleq5_b0b = Rule('q5', '#0#', 'qn', '#', 1, 1)
    ruleq5_b1b = Rule('q5', '#1#', 'qn', '#', 1, 1)
    ruleq5_bb0 = Rule('q5', '##0', 'qn', '#', 1, 1)
    ruleq5_bb1 = Rule('q5', '##1', 'qn', '#', 1, 1)
    ruleq5_bbb = Rule('q5', '###', 'qn', '#', 1, 1)

    ruleq6_000 = Rule('q6', '000', 'q6', '0', 0, -1)
    ruleq6_001 = Rule('q6', '001', 'q6', '0', 0, -1)
    ruleq6_010 = Rule('q6', '010', 'q6', '0', 0, -1)
    ruleq6_011 = Rule('q6', '011', 'q6', '0', 0, -1)
    ruleq6_100 = Rule('q6', '100', 'q6', '1', 0, -1)
    ruleq6_101 = Rule('q6', '101', 'q6', '1', 0, -1)
    ruleq6_110 = Rule('q6', '110', 'q6', '1', 0, -1)
    ruleq6_111 = Rule('q6', '111', 'q6', '1', 0, -1)
    ruleq6_00b = Rule('q6', '00#', 'q6', '0', 0, -1)
    ruleq6_01b = Rule('q6', '01#', 'q6', '0', 0, -1)
    ruleq6_10b = Rule('q6', '10#', 'q6', '1', 0, -1)
    ruleq6_11b = Rule('q6', '11#', 'q6', '1', 0, -1)
    ruleq6_0b0 = Rule('q6', '0#0', 'q6', '0', 0, -1)
    ruleq6_0b1 = Rule('q6', '0#1', 'q6', '0', 0, -1)
    ruleq6_1b0 = Rule('q6', '1#0', 'q6', '1', 0, -1)
    ruleq6_1b1 = Rule('q6', '1#1', 'q6', '1', 0, -1)
    ruleq6_b00 = Rule('q6', '#00', 'q7', '#', 0, 1)
    ruleq6_b01 = Rule('q6', '#01', 'q7', '#', 0, 1)
    ruleq6_b10 = Rule('q6', '#10', 'q7', '#', 0, 1)
    ruleq6_b11 = Rule('q6', '#11', 'q7', '#', 0, 1)
    ruleq6_0bb = Rule('q6', '0##', 'q6', '0', 0, -1)
    ruleq6_1bb = Rule('q6', '1##', 'q6', '1', 0, -1)
    ruleq6_b0b = Rule('q6', '#0#', 'q7', '#', 0, 1)
    ruleq6_b1b = Rule('q6', '#1#', 'q7', '#', 0, 1)
    ruleq6_bb0 = Rule('q6', '##0', 'q7', '#', 0, 1)
    ruleq6_bb1 = Rule('q6', '##1', 'q7', '#', 0, 1)
    ruleq6_bbb = Rule('q6', '###', 'q7', '#', 0, 1)

    ruleq7_000 = Rule('q7', '000', 'q8', '#', 0, -1)
    ruleq7_001 = Rule('q7', '001', 'q8', '#', 0, -1)
    ruleq7_010 = Rule('q7', '010', 'q8', '#', 0, -1)
    ruleq7_011 = Rule('q7', '011', 'q8', '#', 0, -1)
    ruleq7_100 = Rule('q7', '100', 'q9', '#', 0, -1)
    ruleq7_101 = Rule('q7', '101', 'q9', '#', 0, -1)
    ruleq7_110 = Rule('q7', '110', 'q9', '#', 0, -1)
    ruleq7_111 = Rule('q7', '111', 'q9', '#', 0, -1)
    ruleq7_00b = Rule('q7', '00#', 'q8', '#', 0, -1)
    ruleq7_01b = Rule('q7', '01#', 'q8', '#', 0, -1)
    ruleq7_10b = Rule('q7', '10#', 'q9', '#', 0, -1)
    ruleq7_11b = Rule('q7', '11#', 'q9', '#', 0, -1)
    ruleq7_0b0 = Rule('q7', '0#0', 'q8', '#', 0, -1)
    ruleq7_0b1 = Rule('q7', '0#1', 'q8', '#', 0, -1)
    ruleq7_1b0 = Rule('q7', '1#0', 'q9', '#', 0, -1)
    ruleq7_1b1 = Rule('q7', '1#1', 'q9', '#', 0, -1)
    ruleq7_b00 = Rule('q7', '#00', 'q16', '#', 0, -1)
    ruleq7_b01 = Rule('q7', '#01', 'q16', '#', 0, -1)
    ruleq7_b10 = Rule('q7', '#10', 'q16', '#', 0, -1)
    ruleq7_b11 = Rule('q7', '#11', 'q16', '#', 0, -1)
    ruleq7_0bb = Rule('q7', '0##', 'q8', '#', 0, -1)
    ruleq7_1bb = Rule('q7', '1##', 'q9', '#', 0, -1)
    ruleq7_b0b = Rule('q7', '#0#', 'q16', '#', 0, -1)
    ruleq7_b1b = Rule('q7', '#1#', 'q16', '#', 0, -1)
    ruleq7_bb0 = Rule('q7', '##0', 'q16', '#', 0, -1)
    ruleq7_bb1 = Rule('q7', '##1', 'q16', '#', 0, -1)
    ruleq7_bbb = Rule('q7', '###', 'q16', '#', 0, -1)

    ruleq8_000 = Rule('q8', '000', 'qn', '#', 0, -1)
    ruleq8_001 = Rule('q8', '001', 'qn', '#', 0, -1)
    ruleq8_010 = Rule('q8', '010', 'qn', '#', 0, -1)
    ruleq8_011 = Rule('q8', '011', 'qn', '#', 0, -1)
    ruleq8_100 = Rule('q8', '100', 'qn', '#', 0, -1)
    ruleq8_101 = Rule('q8', '101', 'qn', '#', 0, -1)
    ruleq8_110 = Rule('q8', '110', 'qn', '#', 0, -1)
    ruleq8_111 = Rule('q8', '111', 'qn', '#', 0, -1)
    ruleq8_00b = Rule('q8', '00#', 'qn', '#', 0, -1)
    ruleq8_01b = Rule('q8', '01#', 'qn', '#', 0, -1)
    ruleq8_10b = Rule('q8', '10#', 'qn', '#', 0, -1)
    ruleq8_11b = Rule('q8', '11#', 'qn', '#', 0, -1)
    ruleq8_0b0 = Rule('q8', '0#0', 'qn', '#', 0, -1)
    ruleq8_0b1 = Rule('q8', '0#1', 'qn', '#', 0, -1)
    ruleq8_1b0 = Rule('q8', '1#0', 'qn', '#', 0, -1)
    ruleq8_1b1 = Rule('q8', '1#1', 'qn', '#', 0, -1)
    ruleq8_b00 = Rule('q8', '#00', 'q10', '0', 0, 1)
    ruleq8_b01 = Rule('q8', '#01', 'q10', '0', 0, 1)
    ruleq8_b10 = Rule('q8', '#10', 'q10', '0', 0, 1)
    ruleq8_b11 = Rule('q8', '#11', 'q10', '0', 0, 1)
    ruleq8_0bb = Rule('q8', '0##', 'qn', '#', 0, -1)
    ruleq8_1bb = Rule('q8', '1##', 'q10', '0', 0, 1)
    ruleq8_b0b = Rule('q8', '#0#', 'q10', '0', 0, 1)
    ruleq8_b1b = Rule('q8', '#1#', 'q10', '0', 0, 1)
    ruleq8_bb0 = Rule('q8', '##0', 'q10', '0', 0, 1)
    ruleq8_bb1 = Rule('q8', '##1', 'q10', '0', 0, 1)
    ruleq8_bbb = Rule('q8', '###', 'q10', '0', 0, 1)

    ruleq9_000 = Rule('q9', '000', 'qn', '#', 0, -1)
    ruleq9_001 = Rule('q9', '001', 'qn', '#', 0, -1)
    ruleq9_010 = Rule('q9', '010', 'qn', '#', 0, -1)
    ruleq9_011 = Rule('q9', '011', 'qn', '#', 0, -1)
    ruleq9_100 = Rule('q9', '100', 'qn', '#', 0, -1)
    ruleq9_101 = Rule('q9', '101', 'qn', '#', 0, -1)
    ruleq9_110 = Rule('q9', '110', 'qn', '#', 0, -1)
    ruleq9_111 = Rule('q9', '111', 'qn', '#', 0, -1)
    ruleq9_00b = Rule('q9', '00#', 'qn', '#', 0, -1)
    ruleq9_01b = Rule('q9', '01#', 'qn', '#', 0, -1)
    ruleq9_10b = Rule('q9', '10#', 'qn', '#', 0, -1)
    ruleq9_11b = Rule('q9', '11#', 'qn', '#', 0, -1)
    ruleq9_0b0 = Rule('q9', '0#0', 'qn', '#', 0, -1)
    ruleq9_0b1 = Rule('q9', '0#1', 'qn', '#', 0, -1)
    ruleq9_1b0 = Rule('q9', '1#0', 'qn', '#', 0, -1)
    ruleq9_1b1 = Rule('q9', '1#1', 'qn', '#', 0, -1)
    ruleq9_b00 = Rule('q9', '#00', 'q10', '1', 0, 1)
    ruleq9_b01 = Rule('q9', '#01', 'q10', '1', 0, 1)
    ruleq9_b10 = Rule('q9', '#10', 'q10', '1', 0, 1)
    ruleq9_b11 = Rule('q9', '#11', 'q10', '1', 0, 1)
    ruleq9_0bb = Rule('q9', '0##', 'qn', '#', 0, -1)
    ruleq9_1bb = Rule('q9', '1##', 'q10', '1', 0, 1)
    ruleq9_b0b = Rule('q9', '#0#', 'q10', '1', 0, 1)
    ruleq9_b1b = Rule('q9', '#1#', 'q10', '1', 0, 1)
    ruleq9_bb0 = Rule('q9', '##0', 'q10', '1', 0, 1)
    ruleq9_bb1 = Rule('q9', '##1', 'q10', '1', 0, 1)
    ruleq9_bbb = Rule('q9', '###', 'q10', '1', 0, 1)

    ruleq10_000 = Rule('q10', '000', 'qn', '#', 0, -1)
    ruleq10_001 = Rule('q10', '001', 'qn', '#', 0, -1)
    ruleq10_010 = Rule('q10', '010', 'qn', '#', 0, -1)
    ruleq10_011 = Rule('q10', '011', 'qn', '#', 0, -1)
    ruleq10_100 = Rule('q10', '100', 'qn', '#', 0, -1)
    ruleq10_101 = Rule('q10', '101', 'qn', '#', 0, -1)
    ruleq10_110 = Rule('q10', '110', 'qn', '#', 0, -1)
    ruleq10_111 = Rule('q10', '111', 'qn', '#', 0, -1)
    ruleq10_00b = Rule('q10', '00#', 'qn', '#', 0, -1)
    ruleq10_01b = Rule('q10', '01#', 'qn', '#', 0, -1)
    ruleq10_10b = Rule('q10', '10#', 'qn', '#', 0, -1)
    ruleq10_11b = Rule('q10', '11#', 'qn', '#', 0, -1)
    ruleq10_0b0 = Rule('q10', '0#0', 'qn', '#', 0, -1)
    ruleq10_0b1 = Rule('q10', '0#1', 'qn', '#', 0, -1)
    ruleq10_1b0 = Rule('q10', '1#0', 'qn', '#', 0, -1)
    ruleq10_1b1 = Rule('q10', '1#1', 'qn', '#', 0, -1)
    ruleq10_b00 = Rule('q10', '#00', 'q7', '#', 0, 1)
    ruleq10_b01 = Rule('q10', '#01', 'q7', '#', 0, 1)
    ruleq10_b10 = Rule('q10', '#10', 'q7', '#', 0, 1)
    ruleq10_b11 = Rule('q10', '#11', 'q7', '#', 0, 1)
    ruleq10_0bb = Rule('q10', '0##', 'qn', '#', 0, -1)
    ruleq10_1bb = Rule('q10', '1##', 'q7', '#', 0, 1)
    ruleq10_b0b = Rule('q10', '#0#', 'q7', '#', 0, 1)
    ruleq10_b1b = Rule('q10', '#1#', 'q7', '#', 0, 1)
    ruleq10_bb0 = Rule('q10', '##0', 'q7', '#', 0, 1)
    ruleq10_bb1 = Rule('q10', '##1', 'q7', '#', 0, 1)
    ruleq10_bbb = Rule('q10', '###', 'q7', '#', 0, 1)

    ruleq11_000 = Rule('q11', '000', 'q6', '0', 2, -1)
    ruleq11_001 = Rule('q11', '001', 'q6', '1', 2, -1)
    ruleq11_010 = Rule('q11', '010', 'q12', '0', 2, -1)
    ruleq11_011 = Rule('q11', '011', 'q12', '1', 2, -1)
    ruleq11_100 = Rule('q11', '100', 'q6', '0', 2, -1)
    ruleq11_101 = Rule('q11', '101', 'q6', '1', 2, -1)
    ruleq11_110 = Rule('q11', '110', 'q12', '0', 2, -1)
    ruleq11_111 = Rule('q11', '111', 'q12', '1', 2, -1)
    ruleq11_00b = Rule('q11', '00#', 'q6', '#', 2, -1)
    ruleq11_01b = Rule('q11', '01#', 'q12', '#', 2, -1)
    ruleq11_10b = Rule('q11', '10#', 'q6', '#', 2, -1)
    ruleq11_11b = Rule('q11', '11#', 'q12', '#', 2, -1)
    ruleq11_0b0 = Rule('q11', '0#0', 'qy', '0', 2, -1)
    ruleq11_0b1 = Rule('q11', '0#1', 'qy', '1', 2, -1)
    ruleq11_1b0 = Rule('q11', '1#0', 'qy', '0', 2, -1)
    ruleq11_1b1 = Rule('q11', '1#1', 'qy', '1', 2, -1)
    ruleq11_b00 = Rule('q11', '#00', 'q6', '0', 2, -1)
    ruleq11_b01 = Rule('q11', '#01', 'q6', '1', 2, -1)
    ruleq11_b10 = Rule('q11', '#10', 'q12', '0', 2, -1)
    ruleq11_b11 = Rule('q11', '#11', 'q12', '1', 2, -1)
    ruleq11_0bb = Rule('q11', '0##', 'qy', '#', 2, -1)
    ruleq11_1bb = Rule('q11', '1##', 'qy', '#', 2, -1)
    ruleq11_b0b = Rule('q11', '#0#', 'q6', '#', 2, -1)
    ruleq11_b1b = Rule('q11', '#1#', 'q12', '#', 2, -1)
    ruleq11_bb0 = Rule('q11', '##0', 'qy', '0', 2, -1)
    ruleq11_bb1 = Rule('q11', '##1', 'qy', '1', 2, -1)
    ruleq11_bbb = Rule('q11', '###', 'qy', '#', 2, -1)

    ruleq12_000 = Rule('q12', '000', 'q13', '0', 2, 1)
    ruleq12_001 = Rule('q12', '001', 'q13', '1', 2, 1)
    ruleq12_010 = Rule('q12', '010', 'q13', '0', 2, 1)
    ruleq12_011 = Rule('q12', '011', 'q13', '1', 2, 1)
    ruleq12_100 = Rule('q12', '100', 'q13', '0', 2, 1)
    ruleq12_101 = Rule('q12', '101', 'q13', '1', 2, 1)
    ruleq12_110 = Rule('q12', '110', 'q13', '0', 2, 1)
    ruleq12_111 = Rule('q12', '111', 'q13', '1', 2, 1)
    ruleq12_00b = Rule('q12', '00#', 'q13', '#', 2, 1)
    ruleq12_01b = Rule('q12', '01#', 'q13', '#', 2, 1)
    ruleq12_10b = Rule('q12', '10#', 'q13', '#', 2, 1)
    ruleq12_11b = Rule('q12', '11#', 'q13', '#', 2, 1)
    ruleq12_0b0 = Rule('q12', '0#0', 'q13', '0', 2, 1)
    ruleq12_0b1 = Rule('q12', '0#1', 'q13', '1', 2, 1)
    ruleq12_1b0 = Rule('q12', '1#0', 'q13', '0', 2, 1)
    ruleq12_1b1 = Rule('q12', '1#1', 'q13', '1', 2, 1)
    ruleq12_b00 = Rule('q12', '#00', 'q13', '0', 2, 1)
    ruleq12_b01 = Rule('q12', '#01', 'q13', '1', 2, 1)
    ruleq12_b10 = Rule('q12', '#10', 'q13', '0', 2, 1)
    ruleq12_b11 = Rule('q12', '#11', 'q13', '1', 2, 1)
    ruleq12_0bb = Rule('q12', '0##', 'q13', '#', 2, 1)
    ruleq12_1bb = Rule('q12', '1##', 'q13', '#', 2, 1)
    ruleq12_b0b = Rule('q12', '#0#', 'q13', '#', 2, 1)
    ruleq12_b1b = Rule('q12', '#1#', 'q13', '#', 2, 1)
    ruleq12_bb0 = Rule('q12', '##0', 'q13', '0', 2, 1)
    ruleq12_bb1 = Rule('q12', '##1', 'q13', '1', 2, 1)
    ruleq12_bbb = Rule('q12', '###', 'q13', '#', 2, 1)

    ruleq13_000 = Rule('q13', '000', 'q13', '0', 2, -1)
    ruleq13_001 = Rule('q13', '001', 'q13', '1', 2, -1)
    ruleq13_010 = Rule('q13', '010', 'q13', '0', 2, -1)
    ruleq13_011 = Rule('q13', '011', 'q13', '1', 2, -1)
    ruleq13_100 = Rule('q13', '100', 'q13', '1', 2, -1)
    ruleq13_101 = Rule('q13', '101', 'q14', '0', 2, -1)
    ruleq13_110 = Rule('q13', '110', 'q13', '1', 2, -1)
    ruleq13_111 = Rule('q13', '111', 'q14', '0', 2, -1)
    ruleq13_00b = Rule('q13', '00#', 'q13', '0', 2, -1)
    ruleq13_01b = Rule('q13', '01#', 'q13', '0', 2, -1)
    ruleq13_10b = Rule('q13', '10#', 'q13', '1', 2, -1)
    ruleq13_11b = Rule('q13', '11#', 'q13', '1', 2, -1)
    ruleq13_0b0 = Rule('q13', '0#0', 'q13', '0', 2, -1)
    ruleq13_0b1 = Rule('q13', '0#1', 'q13', '1', 2, -1)
    ruleq13_1b0 = Rule('q13', '1#0', 'q13', '1', 2, -1)
    ruleq13_1b1 = Rule('q13', '1#1', 'q14', '0', 2, -1)
    ruleq13_b00 = Rule('q13', '#00', 'q16', '#', 2, 1)
    ruleq13_b01 = Rule('q13', '#01', 'q15', '#', 2, 1)
    ruleq13_b10 = Rule('q13', '#10', 'q15', '#', 2, 1)
    ruleq13_b11 = Rule('q13', '#11', 'q15', '#', 2, 1)
    ruleq13_0bb = Rule('q13', '0##', 'q13', '0', 2, -1)
    ruleq13_1bb = Rule('q13', '1##', 'q13', '1', 2, -1)
    ruleq13_b0b = Rule('q13', '#0#', 'q15', '#', 2, 1)
    ruleq13_b1b = Rule('q13', '#1#', 'q15', '#', 2, 1)
    ruleq13_bb0 = Rule('q13', '##0', 'q15', '#', 2, 1)
    ruleq13_bb1 = Rule('q13', '##1', 'q15', '#', 2, 1)
    ruleq13_bbb = Rule('q13', '###', 'q15', '#', 2, 1)

    ruleq14_000 = Rule('q14', '000', 'q13', '1', 2, -1)
    ruleq14_001 = Rule('q14', '001', 'q14', '0', 2, -1)
    ruleq14_010 = Rule('q14', '010', 'q13', '1', 2, -1)
    ruleq14_011 = Rule('q14', '011', 'q14', '0', 2, -1)
    ruleq14_100 = Rule('q14', '100', 'q14', '0', 2, -1)
    ruleq14_101 = Rule('q14', '101', 'q14', '1', 2, -1)
    ruleq14_110 = Rule('q14', '110', 'q14', '0', 2, -1)
    ruleq14_111 = Rule('q14', '111', 'q14', '1', 2, -1)
    ruleq14_00b = Rule('q14', '00#', 'q13', '1', 2, -1)
    ruleq14_01b = Rule('q14', '01#', 'q13', '1', 2, -1)
    ruleq14_10b = Rule('q14', '10#', 'q14', '0', 2, -1)
    ruleq14_11b = Rule('q14', '11#', 'q14', '0', 2, -1)
    ruleq14_0b0 = Rule('q14', '0#0', 'q13', '1', 2, -1)
    ruleq14_0b1 = Rule('q14', '0#1', 'q14', '0', 2, -1)
    ruleq14_1b0 = Rule('q14', '1#0', 'q14', '0', 2, -1)
    ruleq14_1b1 = Rule('q14', '1#1', 'q14', '1', 2, -1)
    ruleq14_b00 = Rule('q14', '#00', 'q13', '1', 2, -1)
    ruleq14_b01 = Rule('q14', '#01', 'q13', '1', 2, -1)
    ruleq14_b10 = Rule('q14', '#10', 'q13', '1', 2, -1)
    ruleq14_b11 = Rule('q14', '#11', 'q13', '1', 2, -1)
    ruleq14_0bb = Rule('q14', '0##', 'q13', '1', 2, -1)
    ruleq14_1bb = Rule('q14', '1##', 'q14', '0', 2, -1)
    ruleq14_b0b = Rule('q14', '#0#', 'q13', '1', 2, -1)
    ruleq14_b1b = Rule('q14', '#1#', 'q13', '1', 2, -1)
    ruleq14_bb0 = Rule('q14', '##0', 'q13', '1', 2, -1)
    ruleq14_bb1 = Rule('q14', '##1', 'q13', '1', 2, -1)
    ruleq14_bbb = Rule('q14', '###', 'q13', '1', 2, -1)

    ruleq15_000 = Rule('q15', '000', 'q8', '#', 0, -1)
    ruleq15_001 = Rule('q15', '001', 'q8', '#', 0, -1)
    ruleq15_010 = Rule('q15', '010', 'q8', '#', 0, -1)
    ruleq15_011 = Rule('q15', '011', 'q8', '#', 0, -1)
    ruleq15_100 = Rule('q15', '100', 'q9', '#', 0, -1)
    ruleq15_101 = Rule('q15', '101', 'q9', '#', 0, -1)
    ruleq15_110 = Rule('q15', '110', 'q9', '#', 0, -1)
    ruleq15_111 = Rule('q15', '111', 'q9', '#', 0, -1)
    ruleq15_00b = Rule('q15', '00#', 'q8', '#', 0, -1)
    ruleq15_01b = Rule('q15', '01#', 'q8', '#', 0, -1)
    ruleq15_10b = Rule('q15', '10#', 'q9', '#', 0, -1)
    ruleq15_11b = Rule('q15', '11#', 'q9', '#', 0, -1)
    ruleq15_0b0 = Rule('q15', '0#0', 'q8', '#', 0, -1)
    ruleq15_0b1 = Rule('q15', '0#1', 'q8', '#', 0, -1)
    ruleq15_1b0 = Rule('q15', '1#0', 'q9', '#', 0, -1)
    ruleq15_1b1 = Rule('q15', '1#1', 'q9', '#', 0, -1)
    ruleq15_b00 = Rule('q15', '#00', 'q7', '#', 0, 1)
    ruleq15_b01 = Rule('q15', '#01', 'q7', '#', 0, 1)
    ruleq15_b10 = Rule('q15', '#10', 'q7', '#', 0, 1)
    ruleq15_b11 = Rule('q15', '#11', 'q7', '#', 0, 1)
    ruleq15_0bb = Rule('q15', '0##', 'q8', '#', 0, -1)
    ruleq15_1bb = Rule('q15', '1##', 'q9', '#', 0, -1)
    ruleq15_b0b = Rule('q15', '#0#', 'q7', '#', 0, 1)
    ruleq15_b1b = Rule('q15', '#1#', 'q7', '#', 0, 1)
    ruleq15_bb0 = Rule('q15', '##0', 'q7', '#', 0, 1)
    ruleq15_bb1 = Rule('q15', '##1', 'q7', '#', 0, 1)
    ruleq15_bbb = Rule('q15', '###', 'q7', '#', 0, 1)

    ruleq16_000 = Rule('q16', '000', 'q11', '0', 0, -1)
    ruleq16_001 = Rule('q16', '001', 'q11', '0', 0, -1)
    ruleq16_010 = Rule('q16', '010', 'q11', '0', 0, -1)
    ruleq16_011 = Rule('q16', '011', 'q11', '0', 0, -1)
    ruleq16_100 = Rule('q16', '100', 'q11', '1', 0, -1)
    ruleq16_101 = Rule('q16', '101', 'q11', '1', 0, -1)
    ruleq16_110 = Rule('q16', '110', 'q11', '1', 0, -1)
    ruleq16_111 = Rule('q16', '111', 'q11', '1', 0, -1)
    ruleq16_00b = Rule('q16', '00#', 'q11', '0', 0, -1)
    ruleq16_01b = Rule('q16', '01#', 'q11', '0', 0, -1)
    ruleq16_10b = Rule('q16', '10#', 'q11', '1', 0, -1)
    ruleq16_11b = Rule('q16', '11#', 'q11', '1', 0, -1)
    ruleq16_0b0 = Rule('q16', '0#0', 'q11', '0', 0, -1)
    ruleq16_0b1 = Rule('q16', '0#1', 'q11', '0', 0, -1)
    ruleq16_1b0 = Rule('q16', '1#0', 'q11', '1', 0, -1)
    ruleq16_1b1 = Rule('q16', '1#1', 'q11', '1', 0, -1)
    ruleq16_b00 = Rule('q16', '#00', 'q11', '#', 0, -1)
    ruleq16_b01 = Rule('q16', '#01', 'q11', '#', 0, -1)
    ruleq16_b10 = Rule('q16', '#10', 'q11', '#', 0, -1)
    ruleq16_b11 = Rule('q16', '#11', 'q11', '#', 0, -1)
    ruleq16_0bb = Rule('q16', '0##', 'q11', '0', 0, -1)
    ruleq16_1bb = Rule('q16', '1##', 'q11', '1', 0, -1)
    ruleq16_b0b = Rule('q16', '#0#', 'q11', '#', 0, -1)
    ruleq16_b1b = Rule('q16', '#1#', 'q11', '#', 0, -1)
    ruleq16_bb0 = Rule('q16', '##0', 'q11', '#', 0, -1)
    ruleq16_bb1 = Rule('q16', '##1', 'q11', '#', 0, -1)
    ruleq16_bbb = Rule('q16', '###', 'q11', '#', 0, -1)

    # # initializing each row of the turing table
    q0 = TransitionTableRow('q0', [ruleq0_000, ruleq0_001, ruleq0_010, ruleq0_011, ruleq0_100, ruleq0_101, ruleq0_110,
                                   ruleq0_111, ruleq0_00b, ruleq0_01b, ruleq0_10b, ruleq0_11b, ruleq0_0b0, ruleq0_0b1,
                                   ruleq0_1b0, ruleq0_1b1, ruleq0_b00, ruleq0_b01, ruleq0_b10, ruleq0_b11, ruleq0_0bb,
                                   ruleq0_1bb, ruleq0_b0b, ruleq0_b1b, ruleq0_bb0, ruleq0_bb1, ruleq0_bbb ])
    q1 = TransitionTableRow('q1', [ruleq1_000, ruleq1_001, ruleq1_010, ruleq1_011, ruleq1_100, ruleq1_101, ruleq1_110,
                                   ruleq1_111, ruleq1_00b, ruleq1_01b, ruleq1_10b, ruleq1_11b, ruleq1_0b0, ruleq1_0b1,
                                   ruleq1_1b0, ruleq1_1b1, ruleq1_b00, ruleq1_b01, ruleq1_b10, ruleq1_b11, ruleq1_0bb,
                                   ruleq1_1bb, ruleq1_b0b, ruleq1_b1b, ruleq1_bb0, ruleq1_bb1, ruleq1_bbb])
    q2 = TransitionTableRow('q2', [ruleq2_000, ruleq2_001, ruleq2_010, ruleq2_011, ruleq2_100, ruleq2_101, ruleq2_110,
                                   ruleq2_111, ruleq2_00b, ruleq2_01b, ruleq2_10b, ruleq2_11b, ruleq2_0b0, ruleq2_0b1,
                                   ruleq2_1b0, ruleq2_1b1, ruleq2_b00, ruleq2_b01, ruleq2_b10, ruleq2_b11, ruleq2_0bb,
                                   ruleq2_1bb, ruleq2_b0b, ruleq2_b1b, ruleq2_bb0, ruleq2_bb1, ruleq2_bbb])
    q3 = TransitionTableRow('q3', [ruleq3_000, ruleq3_001, ruleq3_010, ruleq3_011, ruleq3_100, ruleq3_101, ruleq3_110,
                                   ruleq3_111, ruleq3_00b, ruleq3_01b, ruleq3_10b, ruleq3_11b, ruleq3_0b0, ruleq3_0b1,
                                   ruleq3_1b0, ruleq3_1b1, ruleq3_b00, ruleq3_b01, ruleq3_b10, ruleq3_b11, ruleq3_0bb,
                                   ruleq3_1bb, ruleq3_b0b, ruleq3_b1b, ruleq3_bb0, ruleq3_bb1, ruleq3_bbb])
    q4 = TransitionTableRow('q4', [ruleq4_000, ruleq4_001, ruleq4_010, ruleq4_011, ruleq4_100, ruleq4_101, ruleq4_110,
                                   ruleq4_111, ruleq4_00b, ruleq4_01b, ruleq4_10b, ruleq4_11b, ruleq4_0b0, ruleq4_0b1,
                                   ruleq4_1b0, ruleq4_1b1, ruleq4_b00, ruleq4_b01, ruleq4_b10, ruleq4_b11, ruleq4_0bb,
                                   ruleq4_1bb, ruleq4_b0b, ruleq4_b1b, ruleq4_bb0, ruleq4_bb1, ruleq4_bbb])
    q5 = TransitionTableRow('q5', [ruleq5_000, ruleq5_001, ruleq5_010, ruleq5_011, ruleq5_100, ruleq5_101, ruleq5_110,
                                   ruleq5_111, ruleq5_00b, ruleq5_01b, ruleq5_10b, ruleq5_11b, ruleq5_0b0, ruleq5_0b1,
                                   ruleq5_1b0, ruleq5_1b1, ruleq5_b00, ruleq5_b01, ruleq5_b10, ruleq5_b11, ruleq5_0bb,
                                   ruleq5_1bb, ruleq5_b0b, ruleq5_b1b, ruleq5_bb0, ruleq5_bb1, ruleq5_bbb])
    q6 = TransitionTableRow('q6', [ruleq6_000, ruleq6_001, ruleq6_010, ruleq6_011, ruleq6_100, ruleq6_101, ruleq6_110,
                                   ruleq6_111, ruleq6_00b, ruleq6_01b, ruleq6_10b, ruleq6_11b, ruleq6_0b0, ruleq6_0b1,
                                   ruleq6_1b0, ruleq6_1b1, ruleq6_b00, ruleq6_b01, ruleq6_b10, ruleq6_b11, ruleq6_0bb,
                                   ruleq6_1bb, ruleq6_b0b, ruleq6_b1b, ruleq6_bb0, ruleq6_bb1, ruleq6_bbb])
    q7 = TransitionTableRow('q7', [ruleq7_000, ruleq7_001, ruleq7_010, ruleq7_011, ruleq7_100, ruleq7_101, ruleq7_110,
                                   ruleq7_111, ruleq7_00b, ruleq7_01b, ruleq7_10b, ruleq7_11b, ruleq7_0b0, ruleq7_0b1,
                                   ruleq7_1b0, ruleq7_1b1, ruleq7_b00, ruleq7_b01, ruleq7_b10, ruleq7_b11, ruleq7_0bb,
                                   ruleq7_1bb, ruleq7_b0b, ruleq7_b1b, ruleq7_bb0, ruleq7_bb1, ruleq7_bbb])
    q8 = TransitionTableRow('q8', [ruleq8_000, ruleq8_001, ruleq8_010, ruleq8_011, ruleq8_100, ruleq8_101, ruleq8_110,
                                   ruleq8_111, ruleq8_00b, ruleq8_01b, ruleq8_10b, ruleq8_11b, ruleq8_0b0, ruleq8_0b1,
                                   ruleq8_1b0, ruleq8_1b1, ruleq8_b00, ruleq8_b01, ruleq8_b10, ruleq8_b11, ruleq8_0bb,
                                   ruleq8_1bb, ruleq8_b0b, ruleq8_b1b, ruleq8_bb0, ruleq8_bb1, ruleq8_bbb])
    q9 = TransitionTableRow('q9', [ruleq9_000, ruleq9_001, ruleq9_010, ruleq9_011, ruleq9_100, ruleq9_101, ruleq9_110,
                                   ruleq9_111, ruleq9_00b, ruleq9_01b, ruleq9_10b, ruleq9_11b, ruleq9_0b0, ruleq9_0b1,
                                   ruleq9_1b0, ruleq9_1b1, ruleq9_b00, ruleq9_b01, ruleq9_b10, ruleq9_b11, ruleq9_0bb,
                                   ruleq9_1bb, ruleq9_b0b, ruleq9_b1b, ruleq9_bb0, ruleq9_bb1, ruleq9_bbb])
    q10 = TransitionTableRow('q10', [ruleq10_000, ruleq10_001, ruleq10_010, ruleq10_011, ruleq10_100, ruleq10_101, ruleq10_110,
                                   ruleq10_111, ruleq10_00b, ruleq10_01b, ruleq10_10b, ruleq10_11b, ruleq10_0b0, ruleq10_0b1,
                                   ruleq10_1b0, ruleq10_1b1, ruleq10_b00, ruleq10_b01, ruleq10_b10, ruleq10_b11, ruleq10_0bb,
                                   ruleq10_1bb, ruleq10_b0b, ruleq10_b1b, ruleq10_bb0, ruleq10_bb1, ruleq10_bbb])
    q11 = TransitionTableRow('q11', [ruleq11_000, ruleq11_001, ruleq11_010, ruleq11_011, ruleq11_100, ruleq11_101, ruleq11_110,
                                   ruleq11_111, ruleq11_00b, ruleq11_01b, ruleq11_10b, ruleq11_11b, ruleq11_0b0, ruleq11_0b1,
                                   ruleq11_1b0, ruleq11_1b1, ruleq11_b00, ruleq11_b01, ruleq11_b10, ruleq11_b11, ruleq11_0bb,
                                   ruleq11_1bb, ruleq11_b0b, ruleq11_b1b, ruleq11_bb0, ruleq11_bb1, ruleq11_bbb])
    q12 = TransitionTableRow('q12', [ruleq12_000, ruleq12_001, ruleq12_010, ruleq12_011, ruleq12_100, ruleq12_101, ruleq12_110,
                                   ruleq12_111, ruleq12_00b, ruleq12_01b, ruleq12_10b, ruleq12_11b, ruleq12_0b0, ruleq12_0b1,
                                   ruleq12_1b0, ruleq12_1b1, ruleq12_b00, ruleq12_b01, ruleq12_b10, ruleq12_b11, ruleq12_0bb,
                                   ruleq12_1bb, ruleq12_b0b, ruleq12_b1b, ruleq12_bb0, ruleq12_bb1, ruleq12_bbb])
    q13 = TransitionTableRow('q13', [ruleq13_000, ruleq13_001, ruleq13_010, ruleq13_011, ruleq13_100, ruleq13_101, ruleq13_110,
                                   ruleq13_111, ruleq13_00b, ruleq13_01b, ruleq13_10b, ruleq13_11b, ruleq13_0b0, ruleq13_0b1,
                                   ruleq13_1b0, ruleq13_1b1, ruleq13_b00, ruleq13_b01, ruleq13_b10, ruleq13_b11, ruleq13_0bb,
                                   ruleq13_1bb, ruleq13_b0b, ruleq13_b1b, ruleq13_bb0, ruleq13_bb1, ruleq13_bbb])
    q14 = TransitionTableRow('q14', [ruleq14_000, ruleq14_001, ruleq14_010, ruleq14_011, ruleq14_100, ruleq14_101, ruleq14_110,
                                   ruleq14_111, ruleq14_00b, ruleq14_01b, ruleq14_10b, ruleq14_11b, ruleq14_0b0, ruleq14_0b1,
                                   ruleq14_1b0, ruleq14_1b1, ruleq14_b00, ruleq14_b01, ruleq14_b10, ruleq14_b11, ruleq14_0bb,
                                   ruleq14_1bb, ruleq14_b0b, ruleq14_b1b, ruleq14_bb0, ruleq14_bb1, ruleq14_bbb])
    q15 = TransitionTableRow('q15', [ruleq15_000, ruleq15_001, ruleq15_010, ruleq15_011, ruleq15_100, ruleq15_101, ruleq15_110,
                                   ruleq15_111, ruleq15_00b, ruleq15_01b, ruleq15_10b, ruleq15_11b, ruleq15_0b0, ruleq15_0b1,
                                   ruleq15_1b0, ruleq15_1b1, ruleq15_b00, ruleq15_b01, ruleq15_b10, ruleq15_b11, ruleq15_0bb,
                                   ruleq15_1bb, ruleq15_b0b, ruleq15_b1b, ruleq15_bb0, ruleq15_bb1, ruleq15_bbb])
    q16 = TransitionTableRow('q16',
                             [ruleq16_000, ruleq16_001, ruleq16_010, ruleq16_011, ruleq16_100, ruleq16_101, ruleq16_110,
                              ruleq16_111, ruleq16_00b, ruleq16_01b, ruleq16_10b, ruleq16_11b, ruleq16_0b0, ruleq16_0b1,
                              ruleq16_1b0, ruleq16_1b1, ruleq16_b00, ruleq16_b01, ruleq16_b10, ruleq16_b11, ruleq16_0bb,
                              ruleq16_1bb, ruleq16_b0b, ruleq16_b1b, ruleq16_bb0, ruleq16_bb1, ruleq16_bbb])

    # initializing the transition table
    table = TransitionTable([q0, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16])
    write_to_output(str(table))

    # initializing the turing machine
    TM = TuringMachine(alphabet, states, table, tapes, blank_symbol, states[0])

    try:
        result = TM.run()

        # write the result of the turing machine
        write_to_output("\nTuring machine successfully ran. Result is: " + result)
        write_to_output("\nOr if you prefer, " + str(binary_to_number(tape_big_val, blank_symbol)) + " * " +
                        str(binary_to_number(tape_small_val, blank_symbol)) + " = " +
                        str(binary_to_number(result, blank_symbol)))
    except RuntimeError:
        write_to_output("Turing machine run failed, is the value for the small tape larger than the value for " +
                        "the big tape?")

    dump_output()
