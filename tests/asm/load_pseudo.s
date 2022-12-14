.text
.globl main
main:
    la $t0, b1  # write address 0x10000000
    lw $t1, 0($t0)  # load -1 to $t1

    lw $t2, b1  # load -1 to $t2

    addi $t2, $t2, 1
    sw $t2, b1  # store 0 to b1

    j main

.data 0x10000000
b1: .word 0xffffffff
