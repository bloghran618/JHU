import math
from HeapSort import heap_sort
from QuickSort import partition_last_elem
from CommonUtils import *
import Counter
import timeit

# input and output file names for this class
input_file = "inputVals.txt"
output_file = "introSortOutput.txt"
counter = 0


def intro_sort(array, depth_limit, low_index, high_index):
    if low_index < high_index:
        write_to_output(output_file, "The depth limit counter is: " + str(depth_limit))
        write_to_output(output_file, "The index range is: " + str(low_index) + "-" + str(high_index))

        # do a heap sort if the depth limit is 0
        if depth_limit == 0:
            write_to_output(output_file, "Depth limit is 0, use heap sort on range " + str(low_index) + "-" + str(high_index))
            subarray = array[low_index:high_index+1]
            write_to_output(output_file, "The subarray to heap sort is: " + str(subarray))
            heap_sort(subarray, output_file)
            place_subarray(subarray, array, low_index)
            write_to_output(output_file, "The array after inserting heapsorted subarray: " + str(array))

            return

        # else do quick sort
        else:
            write_to_output(output_file, "Depth limit is not 0, do quick sort")
            depth_limit -= 1
            partition_index = partition_last_elem(array, low_index, high_index, output_file)
            intro_sort(array, depth_limit, low_index, partition_index-1)
            intro_sort(array, depth_limit, partition_index+1, high_index)
    else:
        return



if __name__ == '__main__':
    # clear the output
    clear_output_file(output_file)

    # read the input values
    vals = read_input(input_file)

    # write the input values to output
    write_to_output(output_file, "The initial vals are:\n" + str(vals))

    # specify recursion depth limit and run introSort
    depth_limit = math.floor(2 * math.log2(len(vals)))

    # run introsort
    intro_sort(vals, depth_limit, 0, len(vals)-1)

    write_to_output(output_file, "The total number of comparisons: " + str(Counter.value))

    # write the sorted list to output
    write_to_output(output_file, "Sorted:\n" + str(vals))

    # write output to console or file
    dump_output(output_file)
