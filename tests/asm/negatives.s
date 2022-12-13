.data 0x10000000
d1:
    .word 0xffffffff
d2:
    .word 0x1234ffff
.globl main
.text
main:
    addi $t0, $0, -1
    sw $t0, 0($gp)
    lw $t1, 0($gp)
    sub $t2, $t1, $t0