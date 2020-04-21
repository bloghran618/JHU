import random


# this class represents one cell of the DTM model
class Rule:
    def __init__(self, q0, read, q1, write, s):
        self.init_state = q0
        self.read = read
        self.new_state = q1
        self.write = write
        self.move_head = s

        # make sure the move head is either 1 or -1
        if self.move_head != 1 and self.move_head != -1:
            raise TypeError("Move head <" + str(self.s) + "> is not 1 or -1")

    def __str__(self):
        return("q0=" + self.init_state + ", read=" + self.read + ", qnew=" + self.new_state +
               ", write=" + self.write + ", s=" + str(self.move_head))


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
            string += (" | read=" + self.rules[key].read + ", qnew=" + self.rules[key].new_state +
                       ", write=" + self.rules[key].write + ", s=" + str(self.rules[key].move_head))
        return string

    def get_rules(self):
        return self.rules


# this class represents the DTM model
class TransitionTable:
    def __init__(self, rows):
        self.state_functions = {}

        # get the alphabet of the first row to check against the other rows
        base_alphabet = []
        for key in rows[0].get_rules():
            base_alphabet.append(rows[0].get_rules()[key].read)

        # check that all row alphabets match to have a complete table
        for row in rows:
            row_alphabet = []
            for key in row.get_rules():
                row_alphabet.append(row.get_rules()[key].read)
            if row_alphabet != base_alphabet:
                raise TypeError("Row alphabets do not match")
            else:
                self.state_functions[row.initial_state] = row

    def __str__(self):
        string = "\nTransition Table: \n"

        string += "Alphabet: "
        random_key, random_row = random.choice(list(self.state_functions.items()))
        for key in random_row.get_rules():
            string += (" | " + random_row.get_rules()[key].read)
        string += "\n"

        for key in self.state_functions:
            string += (str(self.state_functions[key]) + "\n")

        return string

    def get_alphabet(self):
        alphabet = []
        random_key, random_row = random.choice(list(self.state_functions.items()))
        for key in random_row.get_rules():
            alphabet.append(random_row.get_rules()[key].read)
        return alphabet

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

        # represent the tape as a dictionary
        self.tape = {}
        for index, letter in enumerate(Sigma):
            self.tape[index] = letter

        # check that the alphabets match
        if self.alphabet != self.transition_function.get_alphabet():
            raise TypeError("Turing machine alphabet <" + str(self.alphabet) + "> does not equal " +
                            "Transition table alphabet <" + str(self.transition_function.get_alphabet()) + ">")

        # check that the states match
        if self.states != self.transition_function.get_states():
            raise TypeError("Turing machine states <" + str(self.states) + "> does not equal " +
                            "Transition table states <" + str(self.transition_function.get_states()) + ">")

        # check that the contents of the tape are within the given alphabet
        for index in self.tape:
            if not self.tape[index] in self.alphabet:
                raise TypeError("Letter in tape <" + str(self.tape[index]) + "> not in alphabet <" + str(self.alphabet) + ">")

    # convert the tape dictionary to readable string
    def tape_string(self):
        string = ""
        keys = []

        # get the index of each letter on the tape
        for key in self.tape:
            keys.append(key)

        # sort the indicies
        sorted_keys = sorted(keys)

        # write each letter to the string in order
        for key in sorted_keys:
            string += self.tape[key]

        # return the tape string
        return string

    def run(self):
        while True:
            # write some things to output
            write_to_output("\nTurning the Turing machine")
            write_to_output("The current state is: " + self.state)
            write_to_output("The current index is: " + str(self.tape_index))
            write_to_output("The tape looks like: " + self.tape_string())

            # read the value at the current tape index
            try:
                read = self.tape[self.tape_index]
            except KeyError:
                read = self.blank
            write_to_output("read <" + read + "> at tape index " + str(self.tape_index))

            # get the new state, what to write to the tape, and which way to move the read head
            new_state = self.transition_function.state_functions[self.state].rules[read].new_state
            write = self.transition_function.state_functions[self.state].rules[read].write
            s = self.transition_function.state_functions[self.state].rules[read].move_head
            if s == 1:
                right_or_left = "right"
            else:
                right_or_left = "left"
            write_to_output("Change state to <" + new_state + ">, write <" + write + "> and move head " + right_or_left)

            # change state, write value, and move head
            self.state = new_state
            self.tape[self.tape_index] = write
            self.tape_index += s

            # check if we are ready to return
            if self.state == "qn" or self.state == "qy":
                return self.state


def clear_output_file():
    with open('turingMachine.txt', 'a') as output_file:
        output_file.seek(0)
        output_file.truncate()
        output_file.close()


def write_to_output(string):
    with open('turingMachine.txt', 'a') as output_file:
        output_file.write(string + '\n')
        output_file.close()


def dump_output():

    # check if the file is less than 30 lines
    length_of_file = len(open('turingMachine.txt').readlines())
    if length_of_file < 30:

        # if so, write the file to the console
        with open('turingMachine.txt', 'r') as output_file:
            print(output_file.read())
    else:
        print("task complete, see results in turingMachine.txt")


if __name__ == '__main__':
    clear_output_file()

    # initializing the alphabet and set of states for the turing machine
    alphabet = ['0', '1']
    blank_symbol = "#"
    states = ['q0', 'q1', 'q2', 'q3']
    tape = "10100"

    # initializing each rule for the table
    ruleq00 = Rule('q0', '0', 'q0', '0', 1)
    ruleq01 = Rule('q0', '1', 'q0', '1', 1)
    ruleq0b = Rule('q0', '#', 'q1', '#', -1)
    ruleq10 = Rule('q1', '0', 'q2', '#', -1)
    ruleq11 = Rule('q1', '1', 'q3', '#', -1)
    ruleq1b = Rule('q1', '#', 'qn', '#', -1)
    ruleq20 = Rule('q2', '0', 'qy', '#', -1)
    ruleq21 = Rule('q2', '1', 'qn', '#', -1)
    ruleq2b = Rule('q2', '#', 'qn', '#', -1)
    ruleq30 = Rule('q3', '0', 'qn', '#', -1)
    ruleq31 = Rule('q3', '1', 'qn', '#', -1)
    ruleq3b = Rule('q3', '#', 'qn', '#', -1)

    # initializing each row of the turing table
    q0 = TransitionTableRow('q0', [ruleq00, ruleq01, ruleq0b])
    q1 = TransitionTableRow('q1', [ruleq10, ruleq11, ruleq1b])
    q2 = TransitionTableRow('q2', [ruleq20, ruleq21, ruleq2b])
    q3 = TransitionTableRow('q3', [ruleq30, ruleq31, ruleq3b])

    # initializing the transition table
    table = TransitionTable([q0, q1, q2, q3])

    write_to_output(str(table))

    # initializing the turing machine
    TM = TuringMachine(alphabet, states, table, tape, blank_symbol, states[0])
    final_state = TM.run()

    write_to_output("\nTuring machine successfully ran. Final state is: " + final_state)

    dump_output()
