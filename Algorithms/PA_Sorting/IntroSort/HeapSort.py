from CommonUtils import *
import Counter
import timeit

# input and output file names for this class
input_file = "inputVals.txt"
output_file = "heapSortOutput.txt"


# run heap sort on the given array
def heap_sort(array, out_file):
    # build the max heap
    for index in range(len(array)-1, -1, -1):
        heapify(array, len(array), index)

    write_to_output(out_file, "The array after creating the max heap:\n" + str(array))

    for index in range(len(array)-1, 0, -1):
        # pop the top of the max heap to the LHS of the output array
        swap(array, index, 0)
        write_to_output(out_file, "Pop the top of the max heap to index " + str(index) + ":\n" + str(array))

        # heapify the remaining max heap values
        heapify(array, index, 0)
        write_to_output(out_file, "Heapify index 0-" + str(index-1) + ":\n" + str(array))


# heapify starting at root index
def heapify(array, size, parent_index):
    largest_index = parent_index

    # find left and right indicies of parent children
    left_index = 2 * parent_index + 1
    right_index = 2 * parent_index + 2

    # check if left child exists and is greater than parent
    if left_index < size:
        Counter.value += 1
        if array[parent_index] < array[left_index]:
            largest_index = left_index

    # check if right child exists and is greater than parent
    if right_index < size:
        Counter.value += 1
        if array[largest_index] < array[right_index]:
            largest_index = right_index

    # change root if neccessary
    if largest_index != parent_index:
        swap(array, parent_index, largest_index)

        # heapify the root val
        heapify(array, size, largest_index)


if __name__ == '__main__':
    # clear the output
    clear_output_file(output_file)

    # read the input values
    vals = read_input(input_file)

    # write the input values to output
    write_to_output(output_file, "The initial vals are:\n" + str(vals))

    # build the max heap
    heap_sort(vals, output_file)

    write_to_output(output_file, "The total number of comparisons: " + str(Counter.value))

    # write the sorted list to output
    write_to_output(output_file, "Sorted:\n" + str(vals))

    # write output to console or file
    dump_output(output_file)
