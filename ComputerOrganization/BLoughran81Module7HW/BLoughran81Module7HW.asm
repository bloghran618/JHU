.data
numlg:    .asciiz "Please enter the number in the large pool: "
picklg:   .asciiz "Please enter the number count to be picked from the large pool: "
numsm:    .asciiz "Please enter the number in the small pool: "
picksm:   .asciiz "Please enter the number count to be picked from the small pool: "
odds:     .asciiz "The odds of winning the jackpot are 1 in "
stop:     .asciiz "\nStopped."            
            
.globl main
main:                              # odds of winning lottery given 4 inputs
.text

            # prompt the user for arguments

	    li $v0, 4       	    # system call for print_str
            la $a0, numlg          # address of string to print
            syscall                # print the string
            li $v0, 5              # system call for read_int
            syscall                # get int input
            move $s0, $v0          # save input in $s0

            li $v0, 4              # system call for print_str
            la $a0, picklg         # address of the string to print
            syscall                # print the string
            li $v0, 5              # system call for read_int
            syscall                # get int input
            move $s1, $v0          # save input in $s1

            li $v0, 4              # system call for print_str
            la $a0, numsm          # address of the string to print
            syscall                # print the string
            li $v0, 5              # system call for read_int
            syscall                # get int input
            move $s2, $v0          # save input in $s2

            li $v0, 4              # system call for print_str
            la $a0, picksm         # address of the string to print
            syscall                # print the string
            li $v0, 5              # system call for read_int
            syscall                # get int input
            move $s3, $v0          # save input in $s3

            # odds are 1 in: N! / (C! * (N-C)!)
    	    # or (N! / (N-C)!) * 1 / C!
    	    # where N is the number in the pool and
    	    # where C is the number count to be picked from the pool

            move $a0, $s0           # move N to $a0 for smallfact
            move $a1, $s1           # move C to $a1 for smallfact
            jal smallfact           # call smallfact (simplified algebra)
            move $s4, $v0           # save (N! / (N-C)!) 

            move $a0, $s1           # move C to $a0 for factrl
            jal factrl              # call factrl
            move $s5, $v0           # save C!

            move $a0, $s2           # move N to $a0 for smallfact
            move $a1, $s3           # move C to $a1 for smallfact
            jal smallfact           # call smallfact (simplified algebra)
            move $s6, $v0           # save (N! / (N-C)!) 

            move $a0, $s3           # move C to $a0 for factrl
            jal factrl              # call factrl
            move $s7, $v0           # save C!

            # calculate individual combinations

            div $s4, $s5
            mflo $s4
            #mfhi $t5

            div $s6, $s7
            mflo $s6

            # combine odds for small and large pool to get total odds

            mul $s4, $s4, $s6

            # display results to user

            li $v0, 4               # system call for print_str
            la $a0, odds            # address of the string to print
            syscall                 # print the string
            li $v0, 1               # system call for print_int
            la $a0, ($s4)           # address of the calculated odds
            syscall                 # print the int
            li $v0, 4               # system call for print_str
            la $a0, stop            # address of the string to print
            syscall                 # print the string

            li $v0, 10              # system call for exit()
            syscall                 # exit()


######### Factorial Subroutine Fall 2016
#
# Given C, in register $a0;
# calculate C!, store and return the result in register $v0

factrl:     sw $ra, 4($sp)          # save the return address
            sw $a0, 0($sp)          # save the current value of n
            addi $sp, $sp, -8       # move stack pointer
            slti $t0, $a0, 2        # save 1 iteration, n=0 or n=1; n!=1
            beq $t0, $zero, L1      # not less than 2, calculate n(n-1)!
            addi $v0, $zero, 1      # n=1; n!=1
            jr $ra                  # now multiply

L1:         addi $a0, $a0, -1       # n = n-1

            jal factrl              # now (n-1)!

            addi $sp, $sp, 8        # reset the stack pointer
            lw $a0, 0($sp)          # fetch saved (n-1)
            lw $ra, 4($sp)          # fetch return address
            mul $v0, $a0, $v0       # multiply (n)*(n-1)
            jr $ra                  # return value n!

# P Snyder 14 August 2016
######### End of the subroutine

######### Modified Factorial Subroutine Spring 2019
#
# Given N, in register $a0;
# Given C, in register $a1;
# calculate N / (N-C)!, store and return the result in register $v0
            
smallfact:  sw $ra, 8($sp)          # save the return address
            sw $a0, 4($sp)          # save the current value of n
            sw $a1, 0($sp)          # save the current value of r
            li $t0, 1               # create iterator
            move $v0, $a0           # initialize $v0 with N
            bne $a1, 1, L2          # don't loop if C == 1
            #lw $ra, 8($sp)          # fetch return address
            jr $ra                  # return value n!

L2:         addi $t0, $t0, 1        # increment iterator
            addi $a0, $a0, -1       # N -= 1
            mul $v0, $a0, $v0       # set $v0 to $v0 * N
            blt $t0, $a1, L2        # loop again if iterator less than C
            #lw $ra, 8($sp)          # fetch return address
            jr $ra                  # return value n!

# B Loughran 13 March 2019
######### End of the subroutine