#addi $t5,$zero,-2
#addi $t4,$zero,-2
#sra $t5,$t5,3
#xori $t5,$t5,0x9ae3

#addi $t0,$zero,disp

addi $at,$zero,5
addi $a1,$zero,6

addi $t4,$zero,-2147483648
addiu $t5,$t4,-2
andi $t6,$t4,-2

#lwl $t6, $t4
#lwr $t7, $t4

li      $v0, 10              # terminate program run and
syscall
