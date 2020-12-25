def write_output(output_file, string):
    out_file = open(output_file, 'a+')
    out_file.write(str(string) + '\n')
    print(string)
    out_file.close()
