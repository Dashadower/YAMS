.data
m: .word 0x12345678
.text
.globl main
main:
    la $t1, m
    lw $t2, 0($t1)
    nop

    beq $t2, $t0, main
