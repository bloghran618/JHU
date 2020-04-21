.globl main
main: # sum of integers from 1 to 100
.text
add $t0, $zero, $zero # I is zero
add $s4, $zero, $zero # Sum is zero
addi $t1, $zero, 100 # set the limit value (100)
loop:
addi $t0, $t0, 1 # I = I + 1

# multiply logic
add $t2, $zero, $zero # create mult iterator
add $t3, $t0, $zero # store multiply value
add $t4, $zero, $zero # final value will be placed in $t4
mult:
add $t4, $t4, $t3 # final += multiplier
addi $t2, $t2, 1 # multiply iteratior += 1
blt $t2, $t3, mult # I < 100 loop to do again
# end multiply logic

add $s4, $s4, $t4 # Sum = Sum + I
blt $t0, $t1, loop # I < 100 loop to do again
addi $v0, $zero, 4 # print string
la $a0, str # the text for output
syscall # call opsys
addi $v0, $zero, 1 # print integer
add $a0, $zero, $s4 # the integer is Sum
syscall # call opsys
addi $v0, $zero, 4 # print string
la $a0, stopped # the text for output
syscall # call opsys
addi $v0, $zero, 10 # finished .. stop .. return
syscall # to the Operating System
.data
str: .asciiz "The sum of squares of the integers 1 ... 100 is "
stopped:
.asciiz "\nStopped."