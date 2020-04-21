from CommonUtils import *
import Counter
import timeit

# input and output file names for this class
input_file = "inputVals.txt"
output_file = "quickSortOutput.txt"
# counter = 0


# run quicksort on the  given array and range
def quick_sort(array, low_index, high_index):
    if low_index < high_index:
        partition_index = partition_last_elem(array, low_index, high_index, output_file)
        quick_sort(array, low_index, partition_index-1)
        quick_sort(array, partition_index+1, high_index)


# place items less than partition to the left and values greater than partition to right
def partition_last_elem(array, low_index, high_index, out_file):
    write_to_output(out_file, "The range of the partition is: " + str(low_index) + "-" + str(high_index))
    # get the pivot and write some things to output
    pivot = get_pivot_last_elem(array, low_index, high_index)
    write_to_output(out_file, "The pivot is the last value in range: " + str(pivot))

    # check each element in the array to see if it is less than the pivot
    for index in range(low_index, high_index):
        Counter.value += 1

        # if the value is less than the pivot move it to the LHS of the array
        if array[index] <= pivot:
            array = swap(array, low_index, index)
            low_index += 1

    # put the pivot in the pivot position
    array = swap(array, low_index, high_index)
    write_to_output(out_file, "After sending pivot " + str(pivot) + " to index " + str(low_index) + ":\n" + str(array))
    # return the index of the pivot
    return low_index


# designate the last item in the range as the pivot
def get_pivot_last_elem(array, low_index, high_index):
    return array[high_index]


if __name__ == '__main__':
    # clear the output
    clear_output_file(output_file)

    # read the input values
    vals = read_input(input_file)

    # write the input values to output
    write_to_output(output_file, "The initial vals are:\n" + str(vals))

    # sort the values using quicksort
    quick_sort(vals, 0, len(vals)-1)

    write_to_output(output_file, "The total number of comparisons: " + str(Counter.value))

    # write the sorted list to output
    write_to_output(output_file, "Sorted:\n" + str(vals))

    # write output to console or file
    dump_output(output_file)
