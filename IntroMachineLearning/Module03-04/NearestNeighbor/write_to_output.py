def write_output(output_file, string):
    """
    helper function to write file and console output

    :param output_file: the output file or list of output files
    :param string: the string to output
    :return:
    """
    if isinstance(output_file, list):
        for output in output_file:
            # write to all output files in output file list
            out_file = open(output, 'a+')
            out_file.write(str(string) + '\n')
            out_file.close()
    else:
        # write to just the output file


        out_file = open(output_file, 'a+')
        out_file.write(str(string) + '\n')
        out_file.close()
    print(string)
