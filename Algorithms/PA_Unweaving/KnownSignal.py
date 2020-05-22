# this class tracks the known signal
class KnownSignal:

    # initialize the signal
    def __init__(self, signal):
        self.index = 0
        self.signal = signal

    def __str__(self):
        signal_string = "The repeated signal is: " + str(self.signal)
        index_string = "The current index is: " + str(self.index)
        return signal_string + "\n" + index_string

    def get_signal(self):
        return self.signal

    def get_index(self):
        return self.index

    def set_index(self, new_index):
        self.index = new_index

    # add an increment to the signal index and handle wrapping if we go past the end of the signal
    def add_val_and_index(self, val, ind):
        # get the values of the maximum possible index and the current index
        max_index = len(self.signal) - 1
        current_index = ind

        # increment the index by val
        while val > 0:
            # if we go over max index, wrap back to 0
            if current_index + 1 > max_index:
                current_index = 0
            # increment the index by 1
            else:
                current_index += 1

            # decrement val
            val -= 1

        return current_index

    # add a value to the current index, handle wrapping
    def add_val_to_index(self, val):
        new_index = self.add_val_and_index(val, self.index)
        self.index = new_index

    def get_val_at_current_index(self):
        return self.signal[self.index]

    def get_val_at_index(self, index):
        return self.signal[index]

    def get_signal_length(self):
        return len(self.signal)
