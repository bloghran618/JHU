Python Version: 3.6.2

Input File: turingMachineInput.txt
The turingMachineInput.txt file contains just two lines of the following format:

big_number=10101010
little_number=1010

On the first line you specify the larger number of the two numbers to perform the operation on
On the second line you can specify the smaller number of the two numbers to perform the operation on
If you put the larger number on the second line you will likely receive an error
The numbers specified in the input file must be in binary format

Execution: There are 4 .py files in the directory. Each .py file corresponds to a different part of 
the problem. TuringMachine.py corresponds to part a of the problem and implements the simple turing
machine from part 1. turingMachineAdd.py will take the input file and add the two inputs, while 
turingMachineSub.py will take the input file and subtract the smaller number from the first number,
and turingMachineMul will multiply the two numbers together. 

Output: The result of each operation is printed at the end of the output file. Each output file 
exists with the same name as the .py execution file, except with a .txt extension. Each output file
first lists the given inputs including the contents of the tape and the transition table. As the 
turing machine executes, each cycle of the turing machine will also output the current state, the current
index, the contents of each input tape, the contents of the output tape, the value read, and the operation 
performed, e.g. what the state is changed to, what to write, on which tape to write, and where to move 
the read head.
