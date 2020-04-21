#addi $t5,$zero,-2
#addi $t4,$zero,-2
#sra $t5,$t5,3
#xori $t5,$t5,0x9ae3

#addi $t0,$zero,disp

addi $t0,$zero,4294967295
addiu $t1,$t0,4294967296

lui $t2,4294967295

#lwl $t6, $t4
#lwr $t7, $t4

li      $v0, 10              # terminate program run and
syscall
