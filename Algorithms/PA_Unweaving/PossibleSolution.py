# this class represents a possible solution to the unassigned bits
class PossibleSolution:

    # initialize the solution
    def __init__(self, signal, signal_breakdown, final_x_index, final_y_index):
        self.signal = signal
        self.signal_breakdown = signal_breakdown
        self.fin_x_index = final_x_index
        self.fin_y_index = final_y_index

    def __str__(self):
        signal_string = "The candidate signal is: " + str(self.signal)
        signal_breakdown_string = "The candidate signal breakdown is: " + str(self.signal_breakdown)
        x_ind_string = "The x index after applying signal is: " + str(self.fin_x_index)
        y_ind_string = "The y index after applying signal is: " + str(self.fin_y_index)
        return_string = signal_string + "\n" + signal_breakdown_string + "\n" + x_ind_string + "\n" + y_ind_string
        return return_string

    def get_signal(self):
        return self.signal

    def get_signal_breakdown(self):
        return self.signal_breakdown

    def get_fin_x_index(self):
        return self.fin_x_index

    def get_fin_y_index(self):
        return self.fin_y_index