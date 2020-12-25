def write_output(output_file, string):
    """
    helper function to write file and console output

    :param output_file: the output file or list of output files
    :param string: the string to output
    :return:
    """
    out_file = open(output_file, 'a+')
    out_file.write(str(string) + '\n')
    out_file.close()
    print(string)


def write_board_output(output_file, verbose, string):
    """
    helper function to write file and console output

    :param output_file: the output file or list of output files
    :param verbose: whether to write output
    :param string: the string to output
    :return:
    """
    if verbose:
        # write to the output file
        out_file = open(output_file, 'a+')
        out_file.write(str(string) + '\n')
        out_file.close()
        print(string)


def write_board_output_no_newline(output_file, verbose, string):
    """
        helper function to write file and console output

        :param output_file: the output file or list of output files
        :param verbose: whether to write output
        :param string: the string to output
        :return:
        """
    if verbose:
        # write to the output file
        out_file = open(output_file, 'a+')
        out_file.write(str(string))
        out_file.close()
        print(string, end='')


def clear_file_output(filename):
    file = open(filename, 'w')
    file.close()